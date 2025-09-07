import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface Customer {
  id: string;
  name: string;
  email?: string;
  phone: string;
  birth_date: string;
  created_at: string;
  updated_at: string;
}

export interface CustomerCreate {
  name: string;
  email?: string;
  phone: string;
  birth_date: string;
}

@Injectable({
  providedIn: 'root'
})
export class CustomerService {
  constructor(private apiService: ApiService) { }

  // Get all customers
  getCustomers(): Observable<Customer[]> {
    return this.apiService.get<Customer[]>('/customers/customers/');
  }

  // Get customer by ID
  getCustomer(id: string): Observable<Customer> {
    return this.apiService.get<Customer>(`/customers/customers/${id}/`);
  }

  // Create new customer
  createCustomer(customer: CustomerCreate): Observable<Customer> {
    return this.apiService.post<Customer>('/customers/customers/', customer);
  }

  // Update customer
  updateCustomer(id: string, customer: Partial<CustomerCreate>): Observable<Customer> {
    return this.apiService.put<Customer>(`/customers/customers/${id}/`, customer);
  }

  // Delete customer
  deleteCustomer(id: string): Observable<void> {
    return this.apiService.delete<void>(`/customers/customers/${id}/`);
  }

  // Search customers
  searchCustomers(query: string): Observable<Customer[]> {
    return this.apiService.get<Customer[]>(`/customers/customers/search/?q=${encodeURIComponent(query)}`);
  }

  // Get customer's special dates
  getCustomerSpecialDates(id: string): Observable<any[]> {
    return this.apiService.get<any[]>(`/customers/customers/${id}/special-dates/`);
  }

  // Check customer game status
  getCustomerGameStatus(id: string): Observable<{has_played: boolean, first_play_date: string | null}> {
    return this.apiService.get<{has_played: boolean, first_play_date: string | null}>(`/customers/customers/${id}/game-status/`);
  }
}
