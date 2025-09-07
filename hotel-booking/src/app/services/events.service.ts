import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface SpecialDate {
  id: string;
  customer: string;
  customer_name: string;
  customer_phone: string;
  special_date_type: string;
  date: string;
  notes?: string;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface SpecialDateCreate {
  customer: string;
  special_date_type: string;
  date: string;
  notes?: string;
}

export interface Event {
  id: string;
  title: string;
  description: string;
  event_type: string;
  start_date: string;
  end_date: string;
  capacity: number;
  current_bookings: number;
  available_spots: number;
  is_full: boolean;
  price: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface EventBooking {
  id: string;
  event: string;
  event_title: string;
  customer: string;
  customer_name: string;
  booking_date: string;
  number_of_guests: number;
  total_price: number;
  status: string;
  notes?: string;
}

@Injectable({
  providedIn: 'root'
})
export class EventsService {
  constructor(private apiService: ApiService) { }

  // Special Dates
  getSpecialDates(): Observable<PaginatedResponse<SpecialDate>> {
    return this.apiService.get<PaginatedResponse<SpecialDate>>('/events/special-dates/');
  }

  getSpecialDate(id: string): Observable<SpecialDate> {
    return this.apiService.get<SpecialDate>(`/events/special-dates/${id}/`);
  }

  createSpecialDate(specialDate: SpecialDateCreate): Observable<SpecialDate> {
    return this.apiService.post<SpecialDate>('/events/special-dates/', specialDate);
  }

  updateSpecialDate(id: string, specialDate: Partial<SpecialDateCreate>): Observable<SpecialDate> {
    return this.apiService.put<SpecialDate>(`/events/special-dates/${id}/`, specialDate);
  }

  deleteSpecialDate(id: string): Observable<void> {
    return this.apiService.delete<void>(`/events/special-dates/${id}/`);
  }

  getUpcomingSpecialDates(): Observable<SpecialDate[]> {
    return this.apiService.get<SpecialDate[]>('/events/special-dates/upcoming/');
  }

  getThisMonthSpecialDates(): Observable<SpecialDate[]> {
    return this.apiService.get<SpecialDate[]>('/events/special-dates/this-month/');
  }

  getSpecialDatesStats(): Observable<{
    total_dates: number;
    birthday_count: number;
    anniversary_count: number;
    other_count: number;
  }> {
    return this.apiService.get<{
      total_dates: number;
      birthday_count: number;
      anniversary_count: number;
      other_count: number;
    }>('/events/special-dates/stats/');
  }

  // Events
  getEvents(): Observable<Event[]> {
    return this.apiService.get<Event[]>('/events/events/');
  }

  getEvent(id: string): Observable<Event> {
    return this.apiService.get<Event>(`/events/events/${id}/`);
  }

  createEvent(event: Partial<Event>): Observable<Event> {
    return this.apiService.post<Event>('/events/events/', event);
  }

  updateEvent(id: string, event: Partial<Event>): Observable<Event> {
    return this.apiService.put<Event>(`/events/events/${id}/`, event);
  }

  deleteEvent(id: string): Observable<void> {
    return this.apiService.delete<void>(`/events/events/${id}/`);
  }

  bookEvent(eventId: string, customerId: string, numberOfGuests: number = 1): Observable<EventBooking> {
    return this.apiService.post<EventBooking>(`/events/events/${eventId}/book/`, {
      customer_id: customerId,
      number_of_guests: numberOfGuests
    });
  }

  // Event Bookings
  getEventBookings(): Observable<EventBooking[]> {
    return this.apiService.get<EventBooking[]>('/events/bookings/');
  }

  getEventBooking(id: string): Observable<EventBooking> {
    return this.apiService.get<EventBooking>(`/events/bookings/${id}/`);
  }

  updateEventBooking(id: string, booking: Partial<EventBooking>): Observable<EventBooking> {
    return this.apiService.put<EventBooking>(`/events/bookings/${id}/`, booking);
  }

  deleteEventBooking(id: string): Observable<void> {
    return this.apiService.delete<void>(`/events/bookings/${id}/`);
  }
}
