/*
 *
 *  Copyright (C) 2008 -2009  Valerio Valerio <vdv100@gmail.com>
 *
 *
 *  This program is free software; you can redistribute it and/or modify
 *  it under the terms of the GNU General Public License as published by
 *  the Free Software Foundation; either version 2 of the License, or
 *  (at your option) any later version.
 *
 *  This program is distributed in the hope that it will be useful,
 *  but WITHOUT ANY WARRANTY; without even the implied warranty of
 *  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 *  GNU General Public License for more details.
 *
 *  You should have received a copy of the GNU General Public License
 *  along with this program; if not, write to the Free Software
 *  Foundation, Inc., 51 Franklin St, Fifth Floor, Boston, MA  02110-1301  USA
 *
 */



#include <stdio.h>
#include <stdlib.h>
#include <errno.h>
#include <fcntl.h>
#include <unistd.h>
#include <string.h>
#include <malloc.h>
#include <syslog.h>
#include <signal.h>
#include <getopt.h>
#include <netinet/in.h>
#include <sys/types.h> 
#include <sys/poll.h>
#include <sys/ioctl.h>
#include <sys/socket.h>
#include <pthread.h>

#include <bluetooth/bluetooth.h>
#include <bluetooth/hci.h>
#include <bluetooth/hci_lib.h>
#include <bluetooth/l2cap.h>
#include <bluetooth/sdp.h>
#include <bluetooth/hidp.h>


#define L2CAP_PSM_HIDP_CTRL 0x11
#define L2CAP_PSM_HIDP_INTR 0x13

uint8_t cls[3];

int ctrl,intr,csg,isg, class_st=0, connection =0;
char default_class[8];
pthread_t thread;

void error(char *msg)
{
    perror(msg);
    exit(1);
}

int create_socket()
{
	
     int sockfd, portno;
     struct sockaddr_in serv_addr;
    
     sockfd = socket(AF_INET, SOCK_STREAM, 0);

     if (sockfd < 0){
        error("ERROR opening socket");
     }

     bzero((char *) &serv_addr, sizeof(serv_addr));
     portno = 6543;
     serv_addr.sin_family = AF_INET;
     serv_addr.sin_addr.s_addr = INADDR_ANY;
     serv_addr.sin_port = htons(portno);

     if (bind(sockfd, (struct sockaddr *) &serv_addr,sizeof(serv_addr)) < 0){
              error("ERROR on binding");
     }

    return sockfd;

}

int l2cap_connect(bdaddr_t *src, bdaddr_t *dst, unsigned short psm)
{
	struct sockaddr_l2 addr;
	struct l2cap_options opts;
	int sk;

	if ((sk = socket(PF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)) < 0)
		return -1;

	memset(&addr, 0, sizeof(addr));
	addr.l2_family  = AF_BLUETOOTH;
	bacpy(&addr.l2_bdaddr, src);

	if (bind(sk, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
		close(sk);
		return -1;
	}

	memset(&opts, 0, sizeof(opts));
	opts.imtu = HIDP_DEFAULT_MTU;
	opts.omtu = HIDP_DEFAULT_MTU;
	opts.flush_to = 0xffff;

	setsockopt(sk, SOL_L2CAP, L2CAP_OPTIONS, &opts, sizeof(opts));

	memset(&addr, 0, sizeof(addr));
	addr.l2_family  = AF_BLUETOOTH;
	bacpy(&addr.l2_bdaddr, dst);
	addr.l2_psm = htobs(psm);

	if (connect(sk, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
		close(sk);
		return -1;
	}

	return sk;
}

/*From Bluez Utils 3.2*/

static int l2cap_listen(const bdaddr_t *bdaddr, unsigned short psm, int lm, int backlog)
{
	struct sockaddr_l2 addr;
	struct l2cap_options opts;
	int sk;

	if ((sk = socket(PF_BLUETOOTH, SOCK_SEQPACKET, BTPROTO_L2CAP)) < 0)
		return -1;

	memset(&addr, 0, sizeof(addr));
	addr.l2_family = AF_BLUETOOTH;
	bacpy(&addr.l2_bdaddr, bdaddr);
	addr.l2_psm = htobs(psm);

	if (bind(sk, (struct sockaddr *) &addr, sizeof(addr)) < 0) {
		close(sk);
		return -1;
	}

	setsockopt(sk, SOL_L2CAP, L2CAP_LM, &lm, sizeof(lm));

	memset(&opts, 0, sizeof(opts));
	opts.imtu = HIDP_DEFAULT_MTU;
	opts.omtu = HIDP_DEFAULT_MTU;
	opts.flush_to = 0xffff;

	setsockopt(sk, SOL_L2CAP, L2CAP_OPTIONS, &opts, sizeof(opts));

	if (listen(sk, backlog) < 0) {
		close(sk);
		return -1;
	}

	return sk;
}

/*From Bluez Utils 3.2*/

static int l2cap_accept(int sk, bdaddr_t *bdaddr)
{
	struct sockaddr_l2 addr;
	socklen_t addrlen;
	int nsk;

	memset(&addr, 0, sizeof(addr));
	addrlen = sizeof(addr);

	if ((nsk = accept(sk, (struct sockaddr *) &addr, &addrlen)) < 0)
		return -1;

	if (bdaddr)
		bacpy(bdaddr, &addr.l2_bdaddr);

	return nsk;
}

static uint8_t* get_device_class(int hdev)
{
	int s = hci_open_dev(hdev);

	if (s < 0) {
		fprintf(stderr, "Can't open device hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}
	
	if (hci_read_class_of_dev(s, cls, 1000) < 0) {
		fprintf(stderr, "Can't read class of device on hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}
	
	return cls;

}

static void set_device_class(int hdev, char* class)
{

	int s = hci_open_dev(hdev);

	uint32_t cod = strtoul(class, NULL, 16);
	if (hci_write_class_of_dev(s, cod, 2000) < 0) {
		fprintf(stderr, "Can't write local class of device on hci%d: %s (%d)\n",
						hdev, strerror(errno), errno);
		exit(1);
	}

}


int reconnect(char *src, char *dst)
{
	int csk, isk;
	bdaddr_t srcaddr, dstaddr;

	str2ba(src, &srcaddr);
	str2ba(dst, &dstaddr);

	csk = l2cap_connect(&srcaddr, &dstaddr, L2CAP_PSM_HIDP_CTRL);
	if (csk < 0) {
		perror("Can't create HID control channel");
		return 0;
	}

	isk = l2cap_connect(&srcaddr, &dstaddr, L2CAP_PSM_HIDP_INTR);
	if (isk < 0) {
		perror("Can't create HID interrupt channel");
		close(csk);
		return 0;
	}

	ctrl = csk;
	intr = isk;

	connection = 1;
	return 1;

}

int send_event(int modifiers, int val)
{

        unsigned char th[10];
	int n;
	
	th[0] = 0xa1;
	th[1] = 0x01;
	th[2] = modifiers; //1 -left control ,2 - left shift, 4 left alt,5- ctrl+ alt (01 + 04) 8 - left gui, 16 - right control, 32 - right sift, 64 - right alt, 128 - right gui
	th[3] = 0x00;
	th[4] = val; // the key code
	th[5] = 0x00;
	th[6] = 0x00;
	th[7] = 0x00;
	th[8] = 0x00;
	th[9] = 0x00;
	
	
	n = write(intr, th, sizeof(th));
	th[4] = 0x00;
	th[2] = 0x00;
	n = write(intr, th, sizeof(th));
	return n;
}

int send_mouse_event(int btn, int mov_x, int mov_y, int whell)
{

        unsigned char th[6];
	int n;
	
	th[0] = 0xa1;
	th[1] = 0x02;
	th[2] = btn; // 0x01 - left, 0x02 - right, 0x04 - middle, 0x08 - side, 0x10 - extra
	th[3] = mov_x;
	th[4] = mov_y; // the key code
	th[5] = whell;
	

	n = write(intr, th, sizeof(th));
	return n;
	/*th[2] = 0x00; 
	th[3] = 0x00;
	th[4] = 0x00; 
	th[5] = 0x00;
	write(is, th, sizeof(th));*/
}

void open_sock()
{
	int csk, isk,cs,is;
	int lm = 0;

	csk = l2cap_listen(BDADDR_ANY, L2CAP_PSM_HIDP_CTRL, lm, 10);
		if (csk < 0) {
			perror("Can't listen on HID control channel");
			connection = -1;
		}

	isk = l2cap_listen(BDADDR_ANY, L2CAP_PSM_HIDP_INTR, lm, 10);
		if (isk < 0) {
			perror("Can't listen on HID interrupt channel");
			close(csk);
			connection = -1;
		}

	cs = l2cap_accept(csk, NULL);
	
	is = l2cap_accept(isk, NULL);	
	
	csg = csk;
	isg = isk;

	ctrl = cs;
	intr = is;

	connection = 1;

	
}

void init_server()
{
	int hdev = 0;
	int  iret;
	uint8_t* dev_class;
	uint8_t* dev_class2;
	
	//Change device class
	dev_class = get_device_class(0);
	printf("0x%02x%02x%02x\n", dev_class[2], dev_class[1], dev_class[0]);

	sprintf(default_class,"0x%02x%02x%02x\n", dev_class[2], dev_class[1], dev_class[0]);
	printf("%s", default_class);
	
	set_device_class(hdev, "0x0005c0");

	dev_class2 = get_device_class(0);
	printf("Device Class changed to: 0x%02x%02x%02x\n", dev_class2[2], dev_class2[1], dev_class2[0]);
	class_st = 1;
	

    	/* Create thread */
	
     	iret = pthread_create( &thread, NULL, open_sock, NULL);
}



int connection_state()
{
	return connection;
}


int quit_serv()
{
	int hdev = 0;

	if (class_st == 1){

		set_device_class(hdev, default_class);
		printf("Device class changed to: %s\n", default_class);
	}
	close(ctrl);
	close(intr);
	close(csg);
	close(isg);
	
	return 1;

}

void quit_thread()
{
	int hdev = 0;
	int  iret;

	if (class_st == 1){

		set_device_class(hdev, default_class);
		printf("Device class changed to: %s\n", default_class);
	}
	
	iret = pthread_cancel(thread);
	printf("Thread finished\n");

}

