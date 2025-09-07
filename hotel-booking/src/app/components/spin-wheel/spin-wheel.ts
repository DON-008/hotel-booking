import { Component, OnInit } from '@angular/core';
import { Router } from '@angular/router';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { SpinWheelService, Prize as ApiPrize, SpinWheelPlayRequest } from '../../services/spin-wheel.service';
import { CustomerService, Customer as ApiCustomer } from '../../services/customer.service';

interface Customer {
  id?: number;
  customerName: string;
  email: string;
  phone: string;
  birthDate: string;
  createdAt?: string;
}

interface Prize {
  id: number;
  name: string;
  description: string;
  icon: string;
  probability: number;
}

@Component({
  selector: 'app-spin-wheel',
  templateUrl: './spin-wheel.html',
  styleUrls: ['./spin-wheel.scss'],
  imports: [CommonModule, FormsModule],
  standalone: true
})
export class SpinWheelComponent implements OnInit {
  // Customer Data Modal
  showCustomerForm = false;
  loading = false;
  error: string | null = null;
  newCustomer: Customer = {
    customerName: '',
    email: '',
    phone: '',
    birthDate: ''
  };

  // Spin Wheel State
  isSpinning = false;
  canSpin = false;
  currentCustomer: Customer | null = null;
  spinResult: Prize | null = null;
  showResult = false;

  // Prizes
  prizes: Prize[] = [];

  // Mock customers storage (in real app, this would be a service)
  customers: Customer[] = [];
  
  // Track which customers have already played
  playedCustomers: Set<number> = new Set();

  constructor(
    private router: Router,
    private spinWheelService: SpinWheelService,
    private customerService: CustomerService
  ) {}

  ngOnInit() {
    this.loadPrizes();
  }

  loadPrizes() {
    this.loading = true;
    this.error = null;
    this.spinWheelService.getActivePrizes().subscribe({
      next: (data) => {
        this.prizes = data.map(item => ({
          id: parseInt(item.id),
          name: item.name,
          description: item.description,
          icon: item.icon,
          probability: item.probability
        }));
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to load prizes';
        this.loading = false;
        console.error('Error loading prizes:', error);
      }
    });
  }

  // Customer Modal Methods
  toggleCustomerForm(): void {
    this.showCustomerForm = !this.showCustomerForm;
    if (!this.showCustomerForm) {
      this.resetCustomerForm();
    }
  }

  resetCustomerForm(): void {
    this.newCustomer = {
      customerName: '',
      email: '',
      phone: '',
      birthDate: ''
    };
  }

  saveCustomer(): void {
    if (this.isValidCustomerForm()) {
      this.loading = true;
      this.error = null;

      const customerData = {
        name: this.newCustomer.customerName,
        email: this.newCustomer.email || '',
        phone: this.newCustomer.phone,
        birth_date: this.newCustomer.birthDate
      };

      // First, try to create the customer
      this.customerService.createCustomer(customerData).subscribe({
        next: (customer) => {
          // Check if customer has already played
          this.customerService.getCustomerGameStatus(customer.id).subscribe({
            next: (gameStatus) => {
              if (gameStatus.has_played) {
                alert(`Sorry ${customer.name}, you have already played the spin wheel game! 🎰\n\nThis game is only available for first-time players.`);
                this.toggleCustomerForm();
                this.loading = false;
                return;
              }

              // Customer can play
              this.currentCustomer = {
                id: parseInt(customer.id),
                customerName: customer.name,
                email: customer.email || '',
                phone: customer.phone,
                birthDate: customer.birth_date,
                createdAt: customer.created_at
              };
              this.canSpin = true;
              this.toggleCustomerForm();
              this.loading = false;
              alert(`Welcome ${customer.name}! You can now spin the wheel! 🎉`);
            },
            error: (error) => {
              // If no game status found, customer can play
              this.currentCustomer = {
                id: parseInt(customer.id),
                customerName: customer.name,
                email: customer.email || '',
                phone: customer.phone,
                birthDate: customer.birth_date,
                createdAt: customer.created_at
              };
              this.canSpin = true;
              this.toggleCustomerForm();
              this.loading = false;
              alert(`Welcome ${customer.name}! You can now spin the wheel! 🎉`);
            }
          });
        },
        error: (error) => {
          // Customer might already exist, try to find them
          this.customerService.searchCustomers(this.newCustomer.phone).subscribe({
            next: (customers) => {
              if (customers.length > 0) {
                const existingCustomer = customers[0];
                this.customerService.getCustomerGameStatus(existingCustomer.id).subscribe({
                  next: (gameStatus) => {
                    if (gameStatus.has_played) {
                      alert(`Sorry ${existingCustomer.name}, you have already played the spin wheel game! 🎰\n\nThis game is only available for first-time players.`);
                      this.toggleCustomerForm();
                      this.loading = false;
                      return;
                    }

                    // Customer can play
                    this.currentCustomer = {
                      id: parseInt(existingCustomer.id),
                      customerName: existingCustomer.name,
                      email: existingCustomer.email || '',
                      phone: existingCustomer.phone,
                      birthDate: existingCustomer.birth_date,
                      createdAt: existingCustomer.created_at
                    };
                    this.canSpin = true;
                    this.toggleCustomerForm();
                    this.loading = false;
                    alert(`Welcome back ${existingCustomer.name}! You can now spin the wheel! 🎉`);
                  },
                  error: () => {
                    // If no game status found, customer can play
                    this.currentCustomer = {
                      id: parseInt(existingCustomer.id),
                      customerName: existingCustomer.name,
                      email: existingCustomer.email || '',
                      phone: existingCustomer.phone,
                      birthDate: existingCustomer.birth_date,
                      createdAt: existingCustomer.created_at
                    };
                    this.canSpin = true;
                    this.toggleCustomerForm();
                    this.loading = false;
                    alert(`Welcome back ${existingCustomer.name}! You can now spin the wheel! 🎉`);
                  }
                });
              } else {
                this.error = 'Failed to create or find customer';
                this.loading = false;
              }
            },
            error: (error) => {
              this.error = 'Failed to create or find customer';
              this.loading = false;
              console.error('Error with customer:', error);
            }
          });
        }
      });
    }
  }

  isValidCustomerForm(): boolean {
    return !!(this.newCustomer.customerName && this.newCustomer.phone && this.newCustomer.birthDate);
  }

  // Spin Wheel Methods
  spinWheel(): void {
    if (!this.canSpin || this.isSpinning || !this.currentCustomer?.id) {
      return;
    }

    this.isSpinning = true;
    this.canSpin = false;
    this.showResult = false;
    this.spinResult = null;
    this.loading = true;
    this.error = null;

    const playRequest: SpinWheelPlayRequest = {
      customer_id: this.currentCustomer.id.toString()
    };

    this.spinWheelService.playSpinWheel(playRequest).subscribe({
      next: (result) => {
        // Find the prize in our local array
        const prize = this.prizes.find(p => p.name === result.prize.name);
        if (prize) {
          this.spinResult = prize;
        } else {
          // Create a prize object from the API result
          this.spinResult = {
            id: parseInt(result.prize.id),
            name: result.prize.name,
            description: result.prize.description,
            icon: result.prize.icon,
            probability: result.prize.probability
          };
        }

        this.isSpinning = false;
        this.showResult = true;
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to play spin wheel';
        this.isSpinning = false;
        this.loading = false;
        console.error('Error playing spin wheel:', error);
      }
    });
  }

  determineResult(): void {
    // Simple probability-based prize selection
    const random = Math.random() * 100;
    let cumulativeProbability = 0;
    
    for (const prize of this.prizes) {
      cumulativeProbability += prize.probability;
      if (random <= cumulativeProbability) {
        this.spinResult = prize;
        break;
      }
    }

    // Fallback to first prize if something goes wrong
    if (!this.spinResult) {
      this.spinResult = this.prizes[0];
    }
  }

  playAgain(): void {
    // Check if customer has already played
    if (this.currentCustomer?.id && this.playedCustomers.has(this.currentCustomer.id)) {
      alert(`Sorry ${this.currentCustomer.customerName}, you have already played the spin wheel game! 🎰\n\nThis game is only available for first-time players.\n\nThank you for playing!`);
      this.startNewCustomer();
      return;
    }
    
    this.showResult = false;
    this.spinResult = null;
    this.canSpin = true;
  }

  startNewCustomer(): void {
    this.currentCustomer = null;
    this.canSpin = false;
    this.showResult = false;
    this.spinResult = null;
    this.toggleCustomerForm();
  }

  goBack(): void {
    this.router.navigate(['/dashboard']);
  }
}
