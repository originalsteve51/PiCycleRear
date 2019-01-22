
import cmdprocessor
import apa

# main execution block starts here
if __name__ == '__main__':

    try:

        cmd_processor = cmdprocessor.CommandProcessor()
        cmd_processor.process()

    except KeyboardInterrupt:
        print('keyboard interrupt ctrl-c')
    finally:
        print('picycler.py ending')


