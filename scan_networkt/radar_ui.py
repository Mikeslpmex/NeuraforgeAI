import matplotlib.pyplot as plt

class VisualRadar:
    def __init__(self):
        plt.ion() # Modo interactivo
        self.fig, self.ax = plt.subplots(subplot_kw={'projection': 'polar'})
        self.ax.set_theta_zero_location("N") # El 0 está en el Norte
        self.ax.set_theta_direction(-1)    # Sentido horario

    def update_map(self, compass_heading, detected_entities):
        """
        compass_heading: Grados (0-360) del magnetómetro
        detected_entities: Lista de (distancia, angulo_relativo, tipo)
        """
        self.ax.clear()
        self.ax.set_theta_zero_location("N")
        self.ax.set_theta_direction(-1)
        
        # Dibujar nuestra orientación (brújula)
        self.ax.annotate('', xy=(np.radians(compass_heading), 1), 
                         xytext=(0, 0), arrowprops=dict(arrowstyle='->', color='red'))

        for dist, angle, entity_type in detected_entities:
            # Ajustar el ángulo de la entidad según la rotación del sensor
            abs_angle = np.radians(angle)
            color = 'blue' if entity_type == 'person' else 'green'
            self.ax.scatter(abs_angle, dist, c=color, s=100, alpha=0.6)

        self.ax.set_ylim(0, 20) # Rango de 20 metros
        plt.draw()
        plt.pause(0.01)
