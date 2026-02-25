import simpy
import numpy as np
import matplotlib.pyplot as plt

class MM1Queue:
    def __init__(self, env, arrival_rate, service_rate):
        self.env = env
        self.server = simpy.Resource(env, capacity=1)
        self.arrival_rate = arrival_rate  # Ρυθμός Άφιξης
        self.service_rate = service_rate  # Ρυθμός Εξυπηρέτησης
        self.waiting_time = []  # Χρόνος Αναμονής
        self.queue_size = 0  # Μέγεθος Ουράς
        self.total_arrivals = 0  # Συνολικές Άφιξεις
        self.total_service_time = 0  # Συνολικός Χρόνος Εξυπηρέτησης
        self.processor_utilization = 0  # Εκμετάλλευση Επεξεργαστή

    def arrival_process(self):
        while True:
            self.total_arrivals += 1
            self.queue_size += 1
            # Υπολογισμός χρόνου μεταξύ αφίξεων
            inter_arrival_time = np.random.exponential(1 / self.arrival_rate)
            yield self.env.timeout(inter_arrival_time)
            self.env.process(self.service_process())

    def service_process(self):
        arrival_time = self.env.now
        with self.server.request() as request:
            yield request
            self.queue_size -= 1
            # Υπολογισμός χρόνου εξυπηρέτησης
            service_time = np.random.exponential(1 / self.service_rate)
            self.total_service_time += service_time
            self.processor_utilization += service_time
            yield self.env.timeout(service_time)
            self.waiting_time.append(self.env.now - arrival_time)

def simulate_mm1(arrival_rate, service_rate, sim_time):
    env = simpy.Environment()
    mm1 = MM1Queue(env, arrival_rate, service_rate)
    env.process(mm1.arrival_process())
    env.run(until=sim_time)

    if len(mm1.waiting_time) > 0:
        avg_waiting_time = sum(mm1.waiting_time) / len(mm1.waiting_time)
    else:
        avg_waiting_time = 0  #  αν δεν υπάρχουν δεδομένα ,προεπιλεγμένη τιμή

    # Υπολογισμός μέσου μεγέθους ουράς και εκμετάλλευσης επεξεργαστή
    avg_queue_size = mm1.total_service_time / sim_time
    processor_utilization = mm1.processor_utilization / sim_time

    return avg_waiting_time, avg_queue_size, processor_utilization

def theoretical_values(arrival_rate, service_rate):
    rho_values = np.linspace(0.1, 0.9, 9)
    avg_queue_size_theoretical = rho_values / (1 - rho_values)
    processor_utilization_theoretical = rho_values
    avg_waiting_time_theoretical = avg_queue_size_theoretical / arrival_rate
    return rho_values, avg_queue_size_theoretical, processor_utilization_theoretical, avg_waiting_time_theoretical

# Είσοδος παραμέτρων
arrival_rate = float(input("Εισαγωγή ρυθμού άφιξης (λ): "))
service_rate = float(input("Εισαγωγή ρυθμού εξυπηρέτησης (μ): "))
sim_time = float(input("Εισαγωγή χρόνου προσομοίωσης: "))

# Προσομοίωση
rho_values, avg_queue_size_theoretical, processor_utilization_theoretical, avg_waiting_time_theoretical = theoretical_values(arrival_rate, service_rate)
avg_waiting_times_sim = []
avg_queue_sizes_sim = []
processor_utilizations_sim = []

for rho in rho_values:
    avg_waiting_time, avg_queue_size, processor_utilization = simulate_mm1(rho * arrival_rate, service_rate, sim_time)
    avg_waiting_times_sim.append(avg_waiting_time)
    avg_queue_sizes_sim.append(avg_queue_size)
    processor_utilizations_sim.append(processor_utilization)

# Σχεδίαση γραφημάτων
plt.figure(figsize=(15, 5))

# Μέσος Χρόνος Αναμονής  (ρ)
plt.subplot(1, 3, 1)
plt.plot(rho_values, avg_waiting_time_theoretical, label='Θεωρητικός')
plt.plot(rho_values, avg_waiting_times_sim, 'o-', label='Προσομοιωμένος')
plt.xlabel('Παράγοντας Εκμετάλλευσης (ρ)')
plt.ylabel('Μέσος Χρόνος Αναμονής')
plt.title('Μέσος Χρόνος Αναμονής ')
plt.legend()

# Μέσο Μέγεθος Ουράς  (ρ)
plt.subplot(1, 3, 2)
plt.plot(rho_values, avg_queue_size_theoretical, label='Θεωρητικός')
plt.plot(rho_values, avg_queue_sizes_sim, 'o-', label='Προσομοιωμένος')
plt.xlabel('Παράγοντας Εκμετάλλευσης (ρ)')
plt.ylabel('Μέσο Μέγεθος Ουράς')
plt.title('Μέσο Μέγεθος Ουράς ')
plt.legend()

# Χρήση Επεξεργαστή  (ρ)
plt.subplot(1, 3, 3)
plt.plot(rho_values, processor_utilization_theoretical, label='Θεωρητικός')
plt.plot(rho_values, processor_utilizations_sim, 'o-', label='Προσομοιωμένος')
plt.xlabel('Παράγοντας Εκμετάλλευσης (ρ)')
plt.ylabel('Χρήση Επεξεργαστή')
plt.title('Χρήση Επεξεργαστή ')
plt.legend()

plt.tight_layout()
plt.show()
