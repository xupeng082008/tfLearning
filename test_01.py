#!/usr/bin/env python3
#-*- coding:utf-8 -*-
import tensorflow as tf
import numpy as np


x_data = np.float32(np.random.rand(2, 100))
y_data = np.dot([0.100, 0.200], x_data) + 0.300

b = tf.Variable(tf.zeros([1]))
w = tf.Variable(tf.random_uniform([1, 2], -1.0, 1.0))
y = tf.matmul(w, x_data) + b

loss = tf.reduce_mean(tf.square(y - y_data))
optimizer = tf.train.GradientDescentOptimizer(0.5)
train = optimizer.minimize(loss)

#init = tf.initialize_all_variables()
init = tf.global_variables_initializer()

"""start the graph"""
sess = tf.Session()
sess.run(init)

"""run"""
for step in range(0, 201):
    sess.run(train)
    if step % 20 == 0:
        print(step, sess.run(w), sess.run(b))

mat1 = tf.constant([[3., 3.]])
mat2 = tf.constant([[2.], [2.]])

product = tf.matmul(mat1, mat2)

with tf.Session() as sess:
    result = sess.run(product)
    print(result)