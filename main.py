from util.RabbitMQ.RabbitMQ import RabbitMQService

if __name__ == '__main__':
    ser = RabbitMQService()
    ser.init()
    ser.subscribe('activity', ser.new_activity_callback)