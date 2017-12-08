clear all
K = 0.6309;
Z_1dB = 50*sqrt(K+K^3);
Z_5dB = 50*sqrt((1+K^2)/K^3);

Z_1dB_out = 50*K;
Z_5dB_out = 50/K;

R = 50*(K+1/K);