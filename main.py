from util.RabbitMQ.RabbitMQ import RabbitMQService
import time

if __name__ == '__main__':
    ser = RabbitMQService()
    ser.init()
    # time.sleep(5)
    ser.subscribe('test', ser.new_activity_callback)