close all; clear all; clc

cmap = parula(6);
set(groot, 'DefaultAxesFontName', 'Times New Roman');
set(groot, 'DefaultTextFontName', 'Times New Roman');
set(groot, 'DefaultLegendFontName', 'Times New Roman');
set(groot, 'DefaultColorbarFontName', 'Times New Roman');

%% Character Angle vs. Velocity
a = readtable('T_111LT.txt');
b = readtable('T_111HT.txt');
c = readtable('C_111LT.txt');
d = readtable('C_111HT.txt');

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
xlabel('Character Angle, \theta, ^{o}')
ylabel('Velocity, v/c')
legend('300K','1500K','Location','NorthWest')
title('Velocity vs. Character Angle','FontSize',16)
subtitle('Loading Orientation: [-111]','FontSize',12)
grid on

%% Screw Stress vs. Velocity
at = table2array(readtable('T_111S_Screw.txt'));
ac = table2array(readtable('C_111S_Screw.txt'));

st = 161*at(:,1);
vt1 = at(:,2);
vt2 = at(:,3);
vt3 = at(:,4);
vt4 = at(:,5);
vt5 = at(:,6);
vt6 = at(:,7);

sc = -161*ac(:,1);
vc1 = ac(:,2);
vc2 = ac(:,3);
vc3 = ac(:,4);
vc4 = ac(:,5);
vc5 = ac(:,6);
vc6 = ac(:,7);

figure(2)
plot(st,vt1,'Color',cmap(1,:),'LineWidth',2); hold on
plot(st,vt2,'Color',cmap(2,:),'LineWidth',2);
plot(st,vt3,'Color',cmap(3,:),'LineWidth',2);
plot(st,vt4,'Color',cmap(4,:),'LineWidth',2);
plot(st,vt5,'Color',cmap(5,:),'LineWidth',2);
plot(st,vt6,'Color',cmap(6,:),'LineWidth',2);
plot(sc,vc1,'--','Color',cmap(1,:),'LineWidth',2)
plot(sc,vc2,'--','Color',cmap(2,:),'LineWidth',2)
plot(sc,vc3,'--','Color',cmap(3,:),'LineWidth',2)
plot(sc,vc4,'--','Color',cmap(4,:),'LineWidth',2)
plot(sc,vc5,'--','Color',cmap(5,:),'LineWidth',2)
plot(sc,vc6,'--','Color',cmap(6,:),'LineWidth',2)
legend('0K','300K','600K','900K','1200K','1500K','Location','NorthWest')
grid on
xlim([0 4.5])
xlabel('Resolved Shear Stress, \tau, GPa')
ylabel('Velocity, v/c')
title('Stress Velocity: Pure Screw','FontSize',16)
subtitle('Loading Orientation: [-111] | Misorientation Angle: 0^{o}','FontSize',12)

%% Screw Temperature vs. Velocity
a = table2array(readtable('C_111T_Screw.txt'));
b = table2array(readtable('T_111T_Screw.txt'));

T = a(:,1);
vc1 = a(:,2);
vc2 = a(:,3);
vc3 = a(:,4);
vc4 = a(:,5);
vc5 = a(:,6);
vc6 = a(:,7);

T = b(:,1);
vt1 = b(:,2);
vt2 = b(:,3);
vt3 = b(:,4);
vt4 = b(:,5);
vt5 = b(:,6);
vt6 = b(:,7);

figure(3)
plot(T,vt1,'Color',cmap(1,:),'LineWidth',2); hold on
plot(T,vt2,'Color',cmap(2,:),'LineWidth',2)
plot(T,vt3,'Color',cmap(3,:),'LineWidth',2)
plot(T,vt4,'Color',cmap(4,:),'LineWidth',2)
plot(T,vt5,'Color',cmap(5,:),'LineWidth',2)
plot(T,vt6,'Color',cmap(6,:),'LineWidth',2)
plot(T,vc1,'--','Color',cmap(1,:),'LineWidth',2)
plot(T,vc2,'--','Color',cmap(2,:),'LineWidth',2)
plot(T,vc3,'--','Color',cmap(3,:),'LineWidth',2)
plot(T,vc4,'--','Color',cmap(4,:),'LineWidth',2)
plot(T,vc5,'--','Color',cmap(5,:),'LineWidth',2)
plot(T,vc6,'--','Color',cmap(6,:),'LineWidth',2)
legend('0.0 GPa','0.2 GPa','0.4 GPa','0.6 GPa','0.8 GPa','1.0 GPa','Location','NorthWest')
grid on
title('Temp Velocity: Pure Screw','FontSize',16)
subtitle('Loading Orientation: [-111] | Misorientation Angle: 0^{o}','FontSize',12)
xlabel('Temperature, T, K')
ylabel('Velocity, v/c')
xlim([0 3000])

%% Edge Stress vs. Velocity
at = table2array(readtable('T_111S_Edge.txt'));
ac = table2array(readtable('C_111S_Edge.txt'));

st = 161*at(:,1);
vt1 = at(:,2);
vt2 = at(:,3);
vt3 = at(:,4);
vt4 = at(:,5);
vt5 = at(:,6);
vt6 = at(:,7);

sc = -161*ac(:,1);
vc1 = ac(:,2);
vc2 = ac(:,3);
vc3 = ac(:,4);
vc4 = ac(:,5);
vc5 = ac(:,6);
vc6 = ac(:,7);

figure(4)
plot(st,vt1,'Color',cmap(1,:),'LineWidth',2); hold on
plot(st,vt2,'Color',cmap(2,:),'LineWidth',2);
plot(st,vt3,'Color',cmap(3,:),'LineWidth',2);
plot(st,vt4,'Color',cmap(4,:),'LineWidth',2);
plot(st,vt5,'Color',cmap(5,:),'LineWidth',2);
plot(st,vt6,'Color',cmap(6,:),'LineWidth',2);
plot(sc,vc1,'--','Color',cmap(1,:),'LineWidth',2)
plot(sc,vc2,'--','Color',cmap(2,:),'LineWidth',2)
plot(sc,vc3,'--','Color',cmap(3,:),'LineWidth',2)
plot(sc,vc4,'--','Color',cmap(4,:),'LineWidth',2)
plot(sc,vc5,'--','Color',cmap(5,:),'LineWidth',2)
plot(sc,vc6,'--','Color',cmap(6,:),'LineWidth',2)
legend('0K','300K','600K','900K','1200K','1500K','Location','NorthWest')
grid on
xlabel('Resolved Shear Stress, \tau, GPa')
ylabel('Velocity, v/c')
title('Stress Velocity: Pure Edge','FontSize',16)
subtitle('Loading Orientation: [-111] | Misorientation Angle: 90^{o}','FontSize',12)

%% Edge Temperature vs. Velocity
a = table2array(readtable('C_111T_Edge.txt'));
b = table2array(readtable('T_111T_Edge.txt'));

T = a(:,1);
vc1 = a(:,2);
vc2 = a(:,3);
vc3 = a(:,4);
vc4 = a(:,5);
vc5 = a(:,6);
vc6 = a(:,7);

T = b(:,1);
vt1 = b(:,2);
vt2 = b(:,3);
vt3 = b(:,4);
vt4 = b(:,5);
vt5 = b(:,6);
vt6 = b(:,7);

figure(5)
plot(T,vt1,'Color',cmap(1,:),'LineWidth',2); hold on
plot(T,vt2,'Color',cmap(2,:),'LineWidth',2)
plot(T,vt3,'Color',cmap(3,:),'LineWidth',2)
plot(T,vt4,'Color',cmap(4,:),'LineWidth',2)
plot(T,vt5,'Color',cmap(5,:),'LineWidth',2)
plot(T,vt6,'Color',cmap(6,:),'LineWidth',2)
plot(T,vc1,'--','Color',cmap(1,:),'LineWidth',2)
plot(T,vc2,'--','Color',cmap(2,:),'LineWidth',2)
plot(T,vc3,'--','Color',cmap(3,:),'LineWidth',2)
plot(T,vc4,'--','Color',cmap(4,:),'LineWidth',2)
plot(T,vc5,'--','Color',cmap(5,:),'LineWidth',2)
plot(T,vc6,'--','Color',cmap(6,:),'LineWidth',2)
legend('0.0 GPa','0.2 GPa','0.4 GPa','0.6 GPa','0.8 GPa','1.0 GPa','Location','NorthWest')
grid on
title('Temp Velocity: Pure Edge','FontSize',16)
subtitle('Loading Orientation: [-111] | Misorientation Angle: 90^{o}','FontSize',12)
xlabel('Temperature, T, K')
ylabel('Velocity, v/c')