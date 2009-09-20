cdef extern from "hidserv.c":
    
    void init_server()
    int send_key_down(int modifiers, int val)
    int send_key_up()
    int send_mouse_event(int btn, int mov_x, int mov_y, int whell)
    char* client_address()
    int connection_state()
    int reconnect(char *src,char *dst)
    int quit_serv()
    void quit_thread()


def init_hidserver():

   init_server()
   

def send_key(mod, val):

   n = send_key_down(mod,val)
   return n

def release_key():

   n = send_key_up()
   return n

def send_mouse_ev(btn,mov_x,mov_y,whell):

  n = send_mouse_event(btn,mov_x,mov_y,whell)
  return n

def get_client_addr():

  addr = client_address()
  return addr 
	
def connec_state():

  n = connection_state()
  return n

def reConnect(src,dst):

  n = reconnect(src,dst)
  return n


def quit_server():
  
  n = quit_serv()
  return n

def quit():

  quit_thread()

