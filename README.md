# Introduction to Intelligent Vehicles

111-01 NTU CSIE5452 Introduction to Intelligent Vehicles

## hw1

> Homework 1 Question 2 \
> Timing Analysis of the CAN Protocol: Part II

Please download the benchmark "input.dat" from NTU COOL. In the benchmark, the first number is $n$, the number of messages. The second number is $\tau$. Each of the following lines contains the priority ($P_i$), the transmission time ($C_i$), and the period ($T_i$) of each message. You are required to do two things in your submission:

1. You should print out n numbers (one number per line) representing the worst-case response time ($R_i$) of those messages. Note that you need to follow the message ordering in the benchmark, e.g., the first number in the list is the worst-case response time of the first message in the benchmark.
2. You should also print out your source codes. (For your information, my implementation is less than 100 lines.) We may ask you to provide your source codes which must be the same as those on your printout. If the worst-case response times above are correct but the source codes are clearly wrong implementation, it is regarded as academic dishonesty.

It is highly recommended to write your codes well (e.g., capable of dynamically allocating memory based on $n$) so that you can reuse them in Homework 2. Ideally, you can test your implementation with the small benchmark in Question 1 and verify its solution by your implementation. Just do not make the same mistake in Questions 1 and 2.

## hw2

> Homework 2 Question 1 \
> Simulated Annealing for Priority Assignment

Please download the benchmark "input.dat" from NTU COOL. In the benchmark, the first number is $n$, the number of messages. The second number is $\tau$. Each of the following lines contains the priority ($P_i$), the transmission time ($C_i$), and the period ($T_i$) of each message. Now, you are asked to use the Simulated Annealing to decide the priority of each message. The requirements are:

- The objective is to minimize the summation of the worst-case response times of all messages.
- The priority of each message must be an integer in the range $[0, n - 1]$.
- The priority of each message must be unique.
- The worst-case response time of each message must be smaller than or equal to the period of each message.
- The given priorities are the initial solution in the Simulated Annealing.
- We expect the total runtime less than 15 seconds.

You are required to do three things in your submission:

1. You should print out n numbers (one number per line) representing the priorities of those messages. Note that you need to follow the message ordering in the benchmark, e.g., the first number in the list is the priority of the first message in the benchmark.
2. You should print out 1 number representing your objective value (best one during your run).
3. You should also print out your source codes. We may ask you to provide your source codes which must be the same as those on your printout. If the worst-case response times above are correct but the source codes are clearly wrong implementation, it is regarded as academic dishonesty.
