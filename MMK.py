import simpy
import numpy as np
import matplotlib.pyplot as plt

class MMKQueue:
    def __init__(self, env, arrival_rate, service_rate, num_servers):
        self.env = env
        # Δημιουργία μιας λίστας εξυπηρετητών, κάθε ένας με χωρητικότητα 1
        self.servers = [simpy.Resource(env, capacity=1) for _ in range(num_servers)]
        self.arrival_rate = arrival_rate
        self.service_rate = service_rate
        self.waiting_time = []
        self.queue_size = 0
        self.total_arrivals = 0
        self.total_service_time = 0
        self.processor_utilization = 0

    def arrival_process(self):
        while True:
            self.total_arrivals += 1
            self.queue_size += 1
            # Υπολογισμός του χρόνου μεταξύ αφίξεων
            inter_arrival_time = np.random.exponential(1 / self.arrival_rate)
            yield self.env.timeout(inter_arrival_time)
            # Καλέστε τη μέθοδο εξυπηρέτησης
            self.env.process(self.service_process())

    def service_process(self):
        arrival_time = self.env.now
        # Επιλέξτε τον εξυπηρετητή με τη μικρότερη ουρά
        chosen_server = min(range(len(self.servers)), key=lambda i: len(self.servers[i].queue))
        with self.servers[chosen_server].request() as request:
            yield request
            self.queue_size -= 1
            # Υπολογισμός του χρόνου εξυπηρέτησης
            service_time = np.random.exponential(1 / self.service_rate)
            self.total_service_time += service_time
            self.processor_utilization += service_time
            yield self.env.timeout(service_time)
            # Υπολογισμός του χρόνου αναμονής και προσθήκη στη λίστα αναμονής
            self.waiting_time.append(self.env.now - arrival_time)

def simulate_mmk(arrival_rate, service_rate, sim_time, num_servers):
    env = simpy.Environment()
    mmk = MMKQueue(env, arrival_rate, service_rate, num_servers)
    env.process(mmk.arrival_process())
    env.run(until=sim_time)

    if len(mmk.waiting_time) > 0:
        avg_waiting_time = sum(mmk.waiting_time) / len(mmk.waiting_time)
    else:
        avg_waiting_time = 0

    avg_queue_size = mmk.total_service_time / sim_time
    processor_utilization = mmk.processor_utilization / sim_time

    return avg_waiting_time, avg_queue_size, processor_utilization

def theoretical_values_mmk(arrival_rate, service_rate, num_servers):
    rho_values = np.linspace(0.1, 0.9, 9)
    # Υπολογισμός θεωρητικών τιμών με βάση τον τύπο για το M/M/K σύστημα
    avg_queue_size_theoretical = (rho_values ** num_servers) * ((1 - rho_values) / (1 - (rho_values ** (num_servers + 1))))
    processor_utilization_theoretical = rho_values
    avg_waiting_time_theoretical = avg_queue_size_theoretical / (arrival_rate * (1 - rho_values))
    return rho_values, avg_queue_size_theoretical, processor_utilization_theoretical, avg_waiting_time_theoretical

# Είσοδος παραμέτρων
arrival_rate = float(input("Εισαγωγή ρυθμού άφιξης (λ): "))
service_rate = float(input("Εισαγωγή ρυθμού εξυπηρέτησης (μ): "))
sim_time = float(input("Εισαγωγή χρόνου προσομοίωσης: "))
num_servers = int(input("Εισαγωγή αριθμού εξυπηρετητών (K): "))

# Προσομοίωση
rho_values, avg_queue_size_theoretical, processor_utilization_theoretical, avg_waiting_time_theoretical = theoretical_values_mmk(arrival_rate, service_rate, num_servers)
avg_waiting_times_sim = []
avg_queue_sizes_sim = []
processor_utilizations_sim = []

for rho in rho_values:
    avg_waiting_time, avg_queue_size, processor_utilization = simulate_mmk(rho * arrival_rate, service_rate, sim_time, num_servers)
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

# Μέσο Μέγεθος Ουράς (ρ)
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
