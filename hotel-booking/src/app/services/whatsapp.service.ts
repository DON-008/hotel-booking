import { Injectable } from '@angular/core';
import { Observable } from 'rxjs';
import { ApiService } from './api.service';

export interface WhatsAppWishRequest {
  customer_name: string;
  phone: string;
  special_date_type: string;
  custom_message?: string;
  offer_details?: string;
}

export interface WhatsAppMessageRequest {
  phone: string;
  message: string;
}

export interface WhatsAppResponse {
  success: boolean;
  message: string;
  message_id?: string;
  error?: string;
  details?: {
    customer_name: string;
    phone: string;
    special_date_type: string;
  };
}

@Injectable({
  providedIn: 'root'
})
export class WhatsAppService {

  constructor(private apiService: ApiService) { }

  /**
   * Send WhatsApp wish message automatically
   */
  sendWishMessage(request: WhatsAppWishRequest): Observable<WhatsAppResponse> {
    return this.apiService.post<WhatsAppResponse>('/whatsapp/send-wish/', request);
  }

  /**
   * Send custom WhatsApp message
   */
  sendMessage(request: WhatsAppMessageRequest): Observable<WhatsAppResponse> {
    return this.apiService.post<WhatsAppResponse>('/whatsapp/send-message/', request);
  }
}
