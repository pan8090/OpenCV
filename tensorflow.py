import tensorflow as tf
import tensorflow
messsage=tf.constant('welcome to the exciting world of Deep Neural Networks!')
with tf.Session() as sess:
    print(sess.run(messsage).decode())