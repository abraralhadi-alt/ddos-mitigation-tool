import time
import random
import logging

logging.basicConfig(
    filename='firewall.log',
    filemode='a',
    format='%(asctime)s - [%(levelname)s] - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S',
    level=logging.INFO
)

class TokenBucketLimiter:
    def __init__(self, capacity, refill_rate):
        self.capacity= float(capacity)
        self.refill_rate= float(refill_rate)
        self.ip_tokens= {}
        self.ip_last_check= {}
        self.violation_strikes= {}
        self.blocklist= {}
        self.total_dropped_packets= 0

    def allow_request(self, ip_address):
        now= time.time()
        
        if ip_address not in self.ip_tokens:
            self.ip_tokens[ip_address] = self.capacity
            self.ip_last_check[ip_address] = now
            self.violation_strikes[ip_address] = 0

        if ip_address in self.blocklist:
            if now < self.blocklist[ip_address]:
                self.total_dropped_packets += 1
                return "BANNED"
            else: 
                del self.blocklist[ip_address]
                self.violation_strikes[ip_address] = 0
                print(f'\n NOTICE: ban expired for {ip_address}. monitoring restored.')
                
        elapsed= now - self.ip_last_check[ip_address]
        self.ip_last_check[ip_address]= now
        self.ip_tokens[ip_address]= min(self.capacity, self.ip_tokens[ip_address] + (elapsed * self.refill_rate))

        if self.ip_tokens[ip_address] >= 1.0:
            self.ip_tokens[ip_address] -= 1.0
            return "PASS"
        
        self.total_dropped_packets += 1
        self.violation_strikes[ip_address] += 1
        
        if self.violation_strikes[ip_address] >= 5 and ip_address not in self.blocklist:
            self.blocklist[ip_address] = now + 5.0 
            
        return "DROP"
    
    def simulate_network_traffic():
        defender= TokenBucketLimiter(capacity=6, refill_rate=2)
        legitimate_ip = "192.168.1.45"
        attacker_ip = "203.0.113.55"
        
        print("Starting the DDoS Mitigation Tool simulation...")
        print("Normal traffic flow incoming...")
        print("-"* 50)

        for i in range(12):
            time.sleep(random.uniform(0.1, 0.4)) 
            
            if i % 3 == 0:
                user_status = defender.allow_request(legitimate_ip)
                print(f"USER [{legitimate_ip}]: {user_status}")
                
            status = defender.allow_request(attacker_ip)
            if status == "PASS":
                print(f"PASS: Request {i+1} processed successfully.")
            else:
                print(f"BLOCK: Request {i+1} rate limited")
        
        print("\n WARNING: Simulating high-traffic DDoS attack..."")
        print("-"* 50)
        time.sleep(1)

        for i in range(20):
            time.sleep(0.2)
            
            if i % 4 == 0:
                user_status = defender.allow_request(legitimate_ip)
                print(f"USER [{legitimate_ip}]: {user_status}")
                
            status = defender.allow_request(attacker_ip)
            
            if status == "PASS":
                print(f"PASS: Flood request {i+1} bypassed defense.")
            elif status == "DROP":
                print(f"MITIGATED: Flood request {i+1} dropped by rate limiter")
                logging.warning(f"Rate-limit exceeded by {attacker_ip}. Packet dropped.")
            elif status == "BANNED":
                print(f"BANNED: Flood request {i+1} dropped automatically via Firewall Blocklist.")
                logging.critical(f"BANNED HOST ATTEMPT: {attacker_ip} tried to connect while blocked.")

            if defender.total_dropped_packets == 8:
                print(f"\n>>> [CRITICAL ALARM] Drop threshold breached! Total drops: {defender.total_dropped_packets} <<<")
                print(">>> IPS Engine executing automated infrastructure defense protocols... <<<\n")
                defender.total_dropped_packets += 1

if __name__ == "__main__":
    TokenBucketLimiter.simulate_network_traffic()
