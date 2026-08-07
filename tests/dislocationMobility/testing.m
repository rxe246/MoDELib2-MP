close all; clear all; clc

cmap = parula(6);
set(groot, 'DefaultAxesFontName', 'Times New Roman');
set(groot, 'DefaultTextFontName', 'Times New Roman');
set(groot, 'DefaultLegendFontName', 'Times New Roman');
set(groot, 'DefaultColorbarFontName', 'Times New Roman');

%%

a = readtable('alt1_T001LT.txt');
b = readtable('alt1_T001HT.txt');
c = readtable('alt1_C001LT.txt');
d = readtable('alt1_C001HT.txt');

theta1 = table2array(a(:,2));
v1 = table2array(a(:,1));

theta2 = table2array(b(:,2));
v2 = table2array(b(:,1));

theta3 = table2array(c(:,2));
v3 = table2array(c(:,1));

theta4 = table2array(d(:,2));
v4 = table2array(d(:,1));

figure(1)
plot(theta1,v1,'b','LineWidth',2); hold on
plot(theta2,v2,'r','LineWidth',2);
plot(theta3,v3,'--b','LineWidth',1);
plot(theta4,v4,'--r','LineWidth',1);
xlim([0 180]);
grid on
xlabel('Character Angle, \theta, ^{o}')
ylabel('Velocity, v/c')
legend('300K','1500K','Location','NorthWest')
title('Velocity vs. Character Angle','FontSize',16)
subtitle('Loading Orientation: [001]','FontSize',12)
