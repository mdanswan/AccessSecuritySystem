# communication constants
FP_HEADER = 0xEF01
FP_ADDRESS = 0xFFFFFFFF

# instruction constants
COLLECT_FP_IMG = [FP_HEADER, FP_ADDRESS, 0x1, 0x3, 0x1, 0x5]

FP_TXD = 8
FP_RXD = 10
FP_TOUCH = 12

# define Finger Print Sensor constants
FP_BAUD = 57600

# define serial communication
S_PORT = '/dev/ttyS0'
COMM = s.Serial(S_PORT, FP_BAUD)

g.setup(FP_TOUCH, g.IN)

try:
    pack = st.pack("!HIBHBH", *f.COLLECT_FP_IMG)
    COMM.write(pack)
    print(COMM.read())
except Exception as e:
    print(e)