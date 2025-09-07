import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface Offer {
  id: string;
  title: string;
  description: string;
  offer_type: 'percentage' | 'fixed';
  discount_value: number;
  status: 'active' | 'inactive' | 'expired';
  valid_from: string;
  valid_to: string;
  max_usage?: number;
  current_usage: number;
  is_valid: boolean;
  is_available: boolean;
  created_at: string;
  updated_at: string;
}

export interface PaginatedResponse<T> {
  count: number;
  next: string | null;
  previous: string | null;
  results: T[];
}

export interface OfferCreate {
  title: string;
  description: string;
  offer_type: 'percentage' | 'fixed';
  discount_value: number;
  valid_from: string;
  valid_to: string;
  max_usage?: number;
  status?: 'active' | 'inactive' | 'expired';
}

export interface OfferUsage {
  id: string;
  offer: string;
  offer_title: string;
  customer: string;
  customer_name: string;
  used_at: string;
  discount_applied: number;
  order_id?: string;
}

@Injectable({
  providedIn: 'root'
})
export class OffersService {
  constructor(private apiService: ApiService) { }

  // Offers
  getOffers(): Observable<PaginatedResponse<Offer>> {
    return this.apiService.get<PaginatedResponse<Offer>>('/offers/offers/');
  }

  getOffer(id: string): Observable<Offer> {
    return this.apiService.get<Offer>(`/offers/offers/${id}/`);
  }

  createOffer(offer: OfferCreate): Observable<Offer> {
    return this.apiService.post<Offer>('/offers/offers/', offer);
  }

  updateOffer(id: string, offer: Partial<OfferCreate>): Observable<Offer> {
    return this.apiService.put<Offer>(`/offers/offers/${id}/`, offer);
  }

  deleteOffer(id: string): Observable<void> {
    return this.apiService.delete<void>(`/offers/offers/${id}/`);
  }

  getActiveOffers(): Observable<PaginatedResponse<Offer>> {
    return this.apiService.get<PaginatedResponse<Offer>>('/offers/offers/active/');
  }

  getExpiredOffers(): Observable<Offer[]> {
    return this.apiService.get<Offer[]>('/offers/offers/expired/');
  }

  useOffer(offerId: string, customerId: string): Observable<OfferUsage> {
    return this.apiService.post<OfferUsage>(`/offers/offers/${offerId}/use/`, {
      customer_id: customerId
    });
  }

  getOffersStats(): Observable<{
    total_offers: number;
    active_offers: number;
    expired_offers: number;
    total_usage: number;
  }> {
    return this.apiService.get<{
      total_offers: number;
      active_offers: number;
      expired_offers: number;
      total_usage: number;
    }>('/offers/offers/stats/');
  }

  // Offer Usages
  getOfferUsages(): Observable<OfferUsage[]> {
    return this.apiService.get<OfferUsage[]>('/offers/usages/');
  }

  getOfferUsage(id: string): Observable<OfferUsage> {
    return this.apiService.get<OfferUsage>(`/offers/usages/${id}/`);
  }

  updateOfferUsage(id: string, usage: Partial<OfferUsage>): Observable<OfferUsage> {
    return this.apiService.put<OfferUsage>(`/offers/usages/${id}/`, usage);
  }

  deleteOfferUsage(id: string): Observable<void> {
    return this.apiService.delete<void>(`/offers/usages/${id}/`);
  }
}
