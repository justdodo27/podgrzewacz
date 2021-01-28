import matplotlib.pyplot as plt

class Podgrzewacz:
    def __init__(self, Napiecie, Objetosc, Temp_pocz, Temp_zad, Przeplyw, Kp, Ti, Td, Rho=1000, C_wlasc=4200):
        self.kp = Kp  # wzmocnienie regulatora
        self.ti = Ti  # czas zdwojenia
        self.td = Td  # czas wyprzedzania
        self.u_max = Napiecie
        self.v = Objetosc
        self.t0 = Temp_pocz
        self.t = Temp_zad
        self.q = Przeplyw
        self.rho = Rho
        self.c = C_wlasc
        self.temperatury = [self.t0]
        self.e = [self.t - self.temperatury[-1]]
        self.sum_of_e = self.e[0]
        self.r = Napiecie**2/(self.q*self.rho*self.c*(self.t - self.t0))
        self.u = [0]
        self.k1 = (self.t - self.t0)/self.q
        self.k2 = 2*Napiecie/(self.r*self.q*self.rho*self.c)
        self.tcz = (self.v/self.q)/50
    
    def generate_data(self, tp, tsim):
        for n in range(0, int(tsim/tp)):
            self.e.append(self.t - self.temperatury[-1])
            delta_e = self.e[-1] - self.e[n]
            new_u = self.kp*(delta_e + (tp/self.ti)*self.e[n] + (self.td/tp) * delta_e**2) + self.u[-1]
            if new_u > self.u_max:
                new_u = self.u_max
            elif new_u < 0:
                new_u = 0
            self.u.append(new_u)
            delta_t = (-self.k1*self.q + self.t0 + self.u[n]*self.k2)/(self.tcz*n + 1)
            new_temp = self.temperatury[-1] + delta_t
            if new_temp < self.t0:
                new_temp = self.t0
            self.temperatury.append(new_temp)



# grzalka = Podgrzewacz(230, 0.01, 20, 60, 0.0333*10**(-3), 0.45, 2, 0.1)
# grzalka.generate_data(0.1, 10000)

# plt.plot(grzalka.temperatury)
# # plt.plot(grzalka.e)
# # plt.plot(grzalka.u)
# plt.show()