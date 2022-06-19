from subscribers import new_activity_callback, record_result_callback, get_feed_callback
from services import RabbitMQService

if __name__ == '__main__':
    rabbitMQService = RabbitMQService()
    rabbitMQService.init()
    # time.sleep(5)
    rabbitMQService.subscribe(
        'activity', new_activity_callback)
    rabbitMQService.subscribe(
        'engagement', record_result_callback)
    rabbitMQService.subscribe(
        'feed_request', get_feed_callback)

    rabbitMQService.start_consuming()
