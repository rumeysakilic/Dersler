#include <stdio.h>
#include <stdlib.h>
#include <string.h>
#include <rabbitmq-c/amqp.h>
#include <amqp_tcp_socket.h>

int main() {
    // RabbitMQ bağlantısı oluşturma
    amqp_connection_state_t conn = amqp_new_connection();
    amqp_socket_t *socket = amqp_tcp_socket_new(conn);
    
    // RabbitMQ sunucusuna bağlanma
    amqp_socket_open(socket, "localhost", 5672);
    
    // Exchange tanımlama
    amqp_channel_open(conn, 1);
    amqp_rpc_reply_t reply = amqp_get_rpc_reply(conn);
    if (reply.reply_type != AMQP_RESPONSE_NORMAL) {
        fprintf(stderr, "Exchange tanımlama hatası\n");
        return 1;
    }
    
    // Diğer RabbitMQ işlemlerini burada gerçekleştirin
    
    // Bağlantıyı kapatma ve belleği temizleme
    amqp_channel_close(conn, 1, AMQP_REPLY_SUCCESS);
    amqp_connection_close(conn, AMQP_REPLY_SUCCESS);
    amqp_destroy_connection(conn);
    
    return 0;
}