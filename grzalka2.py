class Podgrzewacz:
    def __init__(self, Napiecie, Objetosc, Temp_pocz, Temp_zad, Przeplyw, Kp, Ti, Td, Rho=1000, C_wlasc=4200):
        self.uchyb_ustalony = 0
        self.przeregulowanie = 0
        self.dokladnosc_regulacji = 0
        self.koszty_regulacji = 0

        self.napiecie_max = Napiecie
        self.napiecie_min = 0
        self.napiecia = [self.napiecie_min]
        self.t_zad = Temp_zad
        self.t0 = Temp_pocz
        self.t_max = self.t_zad + 10
        self.temperatury = [self.t0]
        self.V = Objetosc
        self.q = Przeplyw
        self.u_max = 10.0
        self.u_min = 0.0
        self.u = [self.u_min]
        self.kp = Kp
        self.ti = Ti
        self.td = Td
        self.V_rho_c = Objetosc*Rho*C_wlasc
        self.q_rho_c = self.q*Rho*C_wlasc
        self.const1 = (self.napiecie_max - self.napiecie_min)/(self.u_max - self.u_min)
        self.const2 = self.napiecie_min - self.u_min*self.const1
        self.e = [0]
        self.sum_of_e = 0
        self.r = (Napiecie**2/(self.q_rho_c*(self.t_zad - self.t0))) - 2
        self.moc = [(self.napiecia[-1]**2) / self.r]
 
    
    def generate_data(self, tp, tsim):
        for n in range(int(tsim/tp)):
            self.e.append(self.t_zad - self.temperatury[-1])
            self.sum_of_e += self.e[-1]
            delta_e = self.e[-1] - self.e[-2]
            tmp_u = self.kp*(self.e[-1] + tp/self.ti * self.sum_of_e + self.td/tp * delta_e)
            self.u.append(max(float(self.u_min), float(min(self.u_max, tmp_u))))
            self.napiecia.append(max(float(self.napiecie_min), min(float(self.napiecie_max), float(self.const1 * self.u[-1] + self.const2))))
            tmp_temp = 2*((tp/(self.V_rho_c)) * (self.q_rho_c*(self.t0 - self.temperatury[-1]) + (self.napiecia[-1]**2/self.r))) + self.temperatury[-1]
            self.temperatury.append(max(float(self.t0), min(float(self.t_max), float(tmp_temp))))
            self.moc.append((self.napiecia[-1]**2) / self.r)
        self.uchyb_ustalony = self.e[-1]
        self.przeregulowanie = (max(self.temperatury) - self.t_zad)*100/self.t_zad  # wynik w procentach !
        self.dokladnosc_regulacji = sum(map(abs, self.e))
        self.koszty_regulacji = sum(map(abs, self.u))
        for index, temperatura in enumerate(self.temperatury):
            if temperatura <= 0.95*self.t_zad or temperatura >= 1.05*self.t_zad:
                self.czas_regulacji = index*tp/60