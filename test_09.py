#!/usr/bin/env python3
#-*- coding:utf-8 -*-

import tensorflow as tf


with tf.variable_scope('v_scope') as scope1:
    Weights1 = tf.get_variable('Weights', shape=[2, 3])
    #bias1 = tf.Variable([0.52], name='bias')
    bias1 = tf.get_variable('bias', [1])



print(Weights1.name)
print(bias1.name)


with tf.variable_scope('v_scope', reuse=True) as scope2:
    Weights2 = tf.get_variable('Weights')
    bias2 = tf.get_variable('bias', [1])


print(Weights2.name)
print(bias2.name)