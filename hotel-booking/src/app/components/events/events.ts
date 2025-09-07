import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { Router } from '@angular/router';
import { EventsService, SpecialDate as ApiSpecialDate, SpecialDateCreate, PaginatedResponse } from '../../services/events.service';
import { CustomerService, Customer } from '../../services/customer.service';
import { OffersService, Offer, PaginatedResponse as OfferPaginatedResponse } from '../../services/offers.service';
import { WhatsAppService, WhatsAppWishRequest } from '../../services/whatsapp.service';

export interface SpecialDate {
  id?: string; // Changed to string for UUID support
  customerName: string;
  email?: string;
  phone: string;
  specialDateType: string;
  date: string;
  notes?: string;
  createdAt?: string;
}

@Component({
  selector: 'app-events',
  imports: [CommonModule, FormsModule],
  templateUrl: './events.html',
  styleUrl: './events.scss'
})
export class EventsComponent implements OnInit {
  showSpecialDateForm = false;
  isEditMode = false;
  selectedFilter = 'All'; // Filter state
  loading = false;
  error: string | null = null;
  
  // Send Wish Modal
  showSendWishModal = false;
  selectedCustomer: SpecialDate | null = null;
  
  // Customer Modal
  showCustomerForm = false;
  newCustomer = {
    customerName: '',
    email: '',
    phone: '',
    birthDate: ''
  };
  
  sendWishForm = {
    selectedOfferId: '',
    communicationMethod: '',
    customMessage: '',
    includeOffer: false
  };
  
  communicationMethods = [
    { value: 'whatsapp', label: 'WhatsApp', icon: '📱' },
    { value: 'sms', label: 'SMS', icon: '💬' }
  ];
  
  // Mock offers data - in real app, this would come from a service
  availableOffers: any[] = []; // Initialize as empty array, will be populated by API
  
  specialDateTypes = [
    'Birthday',
    'Anniversary',
    'Wedding Anniversary', 
    'First Visit',
    'Graduation',
    'Promotion',
    'Retirement',
    'Other Celebration'
  ];

  newSpecialDate: SpecialDate = {
    customerName: '',
    email: '',
    phone: '',
    specialDateType: '',
    date: '',
    notes: ''
  };

  constructor(
    private router: Router,
    private eventsService: EventsService,
    private customerService: CustomerService,
    private offersService: OffersService,
    private whatsappService: WhatsAppService
  ) {}

  ngOnInit() {
    console.log('EventsComponent ngOnInit called');
    console.log('Initial specialDates:', this.specialDates);
    this.loadSpecialDates();
    this.loadOffers();
  }

  specialDates: SpecialDate[] = [];

  // API Methods
  loadSpecialDates() {
    this.loading = true;
    this.error = null;
    console.log('Loading special dates from API...');
    
    this.eventsService.getSpecialDates().subscribe({
      next: (response: PaginatedResponse<ApiSpecialDate>) => {
        console.log('Special dates API response:', response);
        
        // Handle paginated response - extract results array
        const data = response.results;
        console.log('Extracted data array:', data);
        
        this.specialDates = data.map((item: ApiSpecialDate) => ({
          id: item.id, // Keep as string since it's a UUID
          customerName: item.customer_name,
          email: '', // Not provided by API
          phone: item.customer_phone,
          specialDateType: item.special_date_type,
          date: item.date,
          notes: item.notes,
          createdAt: item.created_at
        }));
        this.loading = false;
        console.log('Mapped special dates:', this.specialDates);
      },
      error: (error) => {
        this.error = 'Failed to load special dates';
        this.loading = false;
        console.error('Error loading special dates:', error);
        console.error('Error details:', error.error);
        console.error('Error status:', error.status);
      }
    });
  }

  loadOffers() {
    console.log('Loading offers from API...');
    
    this.offersService.getOffers().subscribe({
      next: (response: OfferPaginatedResponse<Offer>) => {
        console.log('Offers API response:', response);
        
        // Handle paginated response - extract results array
        const data = response.results;
        console.log('Extracted offers data array:', data);
        
        // Filter to show only active offers for Send Wish modal
        const activeOffers = data.filter((offer: Offer) => offer.status === 'active');
        console.log('Active offers:', activeOffers);
        
        this.availableOffers = activeOffers.map((offer: Offer) => ({
          id: offer.id, // Keep as string since it's a UUID
          title: offer.title,
          discount: offer.discount_value,
          type: offer.offer_type
        }));
        console.log('Mapped available offers for Send Wish:', this.availableOffers);
      },
      error: (error) => {
        console.error('Error loading offers:', error);
        console.error('Error details:', error.error);
        console.error('Error status:', error.status);
      }
    });
  }

  goBack() {
    this.router.navigate(['/dashboard']);
  }

  // Special Dates Methods
  toggleSpecialDateForm() {
    this.showSpecialDateForm = !this.showSpecialDateForm;
    if (!this.showSpecialDateForm) {
      this.resetForm();
    }
  }

  resetForm() {
    this.newSpecialDate = {
      customerName: '',
      email: '',
      phone: '',
      specialDateType: '',
      date: '',
      notes: ''
    };
    this.isEditMode = false;
  }

  saveSpecialDate() {
    if (this.isValidForm()) {
      this.loading = true;
      this.error = null;

      if (this.isEditMode && this.newSpecialDate.id) {
        // Update existing - need to find the customer ID from the existing special date
        const existingSpecialDate = this.specialDates.find(sd => sd.id === this.newSpecialDate.id);
        if (!existingSpecialDate) {
          this.error = 'Special date not found';
          this.loading = false;
          return;
        }
        
        // Find the customer by phone number to get the customer ID
        this.customerService.searchCustomers(this.newSpecialDate.phone).subscribe({
          next: (customers) => {
            if (customers.length === 0) {
              this.error = 'Customer not found';
              this.loading = false;
              return;
            }
            
            const customer = customers[0];
            const updateData: Partial<SpecialDateCreate> = {
              customer: customer.id,
              special_date_type: this.newSpecialDate.specialDateType,
              date: this.newSpecialDate.date,
              notes: this.newSpecialDate.notes
            };
            
            this.eventsService.updateSpecialDate(this.newSpecialDate.id!, updateData).subscribe({
              next: () => {
                this.loadSpecialDates(); // Reload data
                this.toggleSpecialDateForm();
                this.loading = false;
              },
              error: (error) => {
                this.error = 'Failed to update special date';
                this.loading = false;
                console.error('Error updating special date:', error);
              }
            });
          },
          error: (error) => {
            this.error = 'Failed to find customer';
            this.loading = false;
            console.error('Error finding customer:', error);
          }
        });
      } else {
        // Add new - first create customer if needed
        this.createCustomerAndSpecialDate();
      }
    }
  }

  private createCustomerAndSpecialDate() {
    // First, try to find existing customer by phone
    this.customerService.searchCustomers(this.newSpecialDate.phone).subscribe({
      next: (existingCustomers) => {
        if (existingCustomers.length > 0) {
          // Customer exists, use existing customer
          const customer = existingCustomers[0];
          this.createSpecialDateForCustomer(customer);
        } else {
          // Customer doesn't exist, create new one
          const customerData = {
            name: this.newSpecialDate.customerName,
            email: this.newSpecialDate.email || '',
            phone: this.newSpecialDate.phone,
            birth_date: this.newSpecialDate.date // Using the special date as birth date for now
          };

          console.log('Creating customer with data:', customerData);
          
          this.customerService.createCustomer(customerData).subscribe({
            next: (customer) => {
              console.log('Customer created successfully:', customer);
              this.createSpecialDateForCustomer(customer);
            },
            error: (error) => {
              this.error = 'Failed to create customer';
              this.loading = false;
              console.error('Error creating customer:', error);
              console.error('Error details:', error.error);
            }
          });
        }
      },
      error: (error) => {
        // If search fails, try to create customer anyway
        const customerData = {
          name: this.newSpecialDate.customerName,
          email: this.newSpecialDate.email || '',
          phone: this.newSpecialDate.phone,
          birth_date: this.newSpecialDate.date
        };

        console.log('Search failed, creating customer with data:', customerData);
        
        this.customerService.createCustomer(customerData).subscribe({
          next: (customer) => {
            console.log('Customer created successfully:', customer);
            this.createSpecialDateForCustomer(customer);
          },
          error: (error) => {
            this.error = 'Failed to create customer';
            this.loading = false;
            console.error('Error creating customer:', error);
            console.error('Error details:', error.error);
          }
        });
      }
    });
  }

  private createSpecialDateForCustomer(customer: any) {
    // Create special date for the customer
    const specialDateData: SpecialDateCreate = {
      customer: customer.id,
      special_date_type: this.newSpecialDate.specialDateType,
      date: this.newSpecialDate.date,
      notes: this.newSpecialDate.notes
    };

    console.log('Creating special date with data:', specialDateData);
    console.log('Customer ID:', customer.id, 'Type:', typeof customer.id);

    this.eventsService.createSpecialDate(specialDateData).subscribe({
      next: () => {
        this.loadSpecialDates(); // Reload data
        this.toggleSpecialDateForm();
        this.loading = false;
      },
      error: (error) => {
        this.error = 'Failed to create special date';
        this.loading = false;
        console.error('Error creating special date:', error);
        console.error('Error details:', error.error);
      }
    });
  }

  editSpecialDate(specialDate: SpecialDate) {
    this.newSpecialDate = { ...specialDate };
    this.isEditMode = true;
    this.showSpecialDateForm = true;
  }

  deleteSpecialDate(id: string) {
    if (confirm('Are you sure you want to delete this special date?')) {
      this.loading = true;
      this.error = null;
      
      this.eventsService.deleteSpecialDate(id).subscribe({
        next: () => {
          this.loadSpecialDates(); // Reload data
          this.loading = false;
        },
        error: (error) => {
          this.error = 'Failed to delete special date';
          this.loading = false;
          console.error('Error deleting special date:', error);
        }
      });
    }
  }

  isValidForm(): boolean {
    return !!(this.newSpecialDate.customerName && 
              this.newSpecialDate.phone && 
              this.newSpecialDate.specialDateType && 
              this.newSpecialDate.date);
  }

  getUpcomingDates(): SpecialDate[] {
    const today = new Date();
    const thirtyDaysFromNow = new Date();
    thirtyDaysFromNow.setDate(today.getDate() + 30);
    
    return this.specialDates.filter(sd => {
      const specialDate = new Date(sd.date);
      return specialDate >= today && specialDate <= thirtyDaysFromNow;
    }).sort((a, b) => new Date(a.date).getTime() - new Date(b.date).getTime());
  }

  getThisMonthDates(): SpecialDate[] {
    const today = new Date();
    const firstDayOfMonth = new Date(today.getFullYear(), today.getMonth(), 1);
    const lastDayOfMonth = new Date(today.getFullYear(), today.getMonth() + 1, 0);
    
    return this.specialDates.filter(sd => {
      const specialDate = new Date(sd.date);
      return specialDate >= firstDayOfMonth && specialDate <= lastDayOfMonth;
    });
  }

  getBirthdayCount(): number {
    return this.specialDates.filter(sd => sd.specialDateType === 'Birthday').length;
  }

  getWeddingAnniversaryCount(): number {
    return this.specialDates.filter(sd => sd.specialDateType === 'Wedding Anniversary').length;
  }

  getAnniversaryCount(): number {
    return this.specialDates.filter(sd => sd.specialDateType === 'Anniversary').length;
  }

  // Filter methods
  setFilter(filter: string): void {
    this.selectedFilter = filter;
  }

  getFilteredSpecialDates(): SpecialDate[] {
    console.log('getFilteredSpecialDates called with filter:', this.selectedFilter);
    console.log('specialDates array:', this.specialDates);
    
    if (this.selectedFilter === 'All') {
      console.log('Returning all special dates:', this.specialDates);
      return this.specialDates;
    }
    
    const filtered = this.specialDates.filter(sd => sd.specialDateType === this.selectedFilter);
    console.log('Filtered special dates:', filtered);
    return filtered;
  }

  getFilterTitle(): string {
    return this.selectedFilter === 'All' ? 'All Special Dates' : `${this.selectedFilter} Dates`;
  }

  sendWish(specialDate: SpecialDate): void {
    this.selectedCustomer = specialDate;
    this.showSendWishModal = true;
    this.resetSendWishForm();
  }

  // Send Wish Modal Methods
  toggleSendWishModal(): void {
    this.showSendWishModal = !this.showSendWishModal;
    if (!this.showSendWishModal) {
      this.resetSendWishForm();
      this.selectedCustomer = null;
    }
  }

  resetSendWishForm(): void {
    this.sendWishForm = {
      selectedOfferId: '',
      communicationMethod: '',
      customMessage: '',
      includeOffer: false
    };
  }

  getSelectedOffer() {
    return this.availableOffers.find(offer => offer.id.toString() === this.sendWishForm.selectedOfferId);
  }

  isWishFormValid(): boolean {
    if (!this.sendWishForm.communicationMethod) {
      return false;
    }
    
    // If includeOffer is checked, then selectedOfferId is required
    if (this.sendWishForm.includeOffer && !this.sendWishForm.selectedOfferId) {
      return false;
    }
    
    return true;
  }

  sendWishMessage(): void {
    if (this.isWishFormValid() && this.selectedCustomer) {
      const customer = this.selectedCustomer;
      const method = this.sendWishForm.communicationMethod;
      const message = this.sendWishForm.customMessage;
      const includeOffer = this.sendWishForm.includeOffer;
      
      let offerDetails = '';
      let offerInfo = '';
      
      if (includeOffer && this.sendWishForm.selectedOfferId) {
        const selectedOffer = this.getSelectedOffer();
        offerDetails = `Special Offer: ${selectedOffer?.title} - ${selectedOffer?.discount}${selectedOffer?.type === 'percentage' ? '%' : '$'} off`;
        offerInfo = `Offer: ${selectedOffer?.title} (${selectedOffer?.discount}${selectedOffer?.type === 'percentage' ? '%' : '$'} off)`;
      }

      // Handle different communication methods
      const communication = this.communicationMethods.find(m => m.value === this.sendWishForm.communicationMethod);
      
      if (method === 'whatsapp') {
        // Send via backend WhatsApp service
        const whatsappRequest: WhatsAppWishRequest = {
          customer_name: customer.customerName,
          phone: customer.phone,
          special_date_type: customer.specialDateType,
          custom_message: message || '',
          offer_details: offerDetails || ''
        };
        
        this.whatsappService.sendWishMessage(whatsappRequest).subscribe({
          next: (response) => {
            if (response.success) {
              const alertMessage = `
                🎉 ${customer.specialDateType} Wishes Sent via WhatsApp!
                
                Customer: ${customer.customerName}
                ${offerInfo ? offerInfo + '\n' : ''}Method: ${communication?.label} ${communication?.icon}
                Phone: ${customer.phone}
                ${message ? '\nCustom Message: ' + message : ''}
                Message ID: ${response.message_id}
              `;
              
              alert(alertMessage);
              console.log('WhatsApp wish sent successfully:', response);
            } else {
              alert(`❌ Failed to send WhatsApp message: ${response.error || response.message}`);
              console.error('WhatsApp send failed:', response);
            }
            this.toggleSendWishModal();
          },
          error: (error) => {
            alert(`❌ Error sending WhatsApp message: ${error.message || 'Unknown error'}`);
            console.error('WhatsApp service error:', error);
            this.toggleSendWishModal();
          }
        });
        
      } else if (method === 'sms') {
        // For SMS, we can still use the browser method or implement backend SMS service
        this.sendSMSMessage(customer.phone, this.createSMSMessage(customer, message, offerDetails));
        
        const alertMessage = `
          🎉 ${customer.specialDateType} Wishes Sent via SMS!
          
          Customer: ${customer.customerName}
          ${offerInfo ? offerInfo + '\n' : ''}Method: ${communication?.label} ${communication?.icon}
          Phone: ${customer.phone}
          ${message ? '\nCustom Message: ' + message : ''}
        `;
        
        alert(alertMessage);
        this.toggleSendWishModal();
      }
    }
  }

  // Helper method to create SMS message
  createSMSMessage(customer: SpecialDate, customMessage: string, offerDetails: string): string {
    let message = `🎉 Happy ${customer.specialDateType}! ${customer.customerName}, we're thinking of you on your special day!`;
    
    if (offerDetails) {
      message += `\n\n🎁 ${offerDetails}`;
    }
    
    if (customMessage) {
      message += `\n\n💝 ${customMessage}`;
    }
    
    message += `\n\nBest wishes from your friends at [Hotel Name]!`;
    
    return message;
  }

  // SMS Integration (fallback for non-WhatsApp)
  sendSMSMessage(phoneNumber: string, message: string): void {
    // Clean phone number
    const cleanPhone = phoneNumber.replace(/[^\d+]/g, '');
    
    // Create SMS URL
    const smsUrl = `sms:${cleanPhone}?body=${encodeURIComponent(message)}`;
    
    // Open SMS app
    window.open(smsUrl, '_blank');
    
    console.log('SMS message prepared:', {
      phone: cleanPhone,
      message: message,
      url: smsUrl
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

      console.log('Creating customer with data:', customerData);
      
      this.customerService.createCustomer(customerData).subscribe({
        next: (customer) => {
          console.log('Customer created successfully:', customer);
          
          // Add customer to the special dates list as a birthday entry
          const specialDate: SpecialDate = {
            id: customer.id, // Keep as string since it's a UUID
            customerName: customer.name,
            email: customer.email,
            phone: customer.phone,
            specialDateType: 'Birthday',
            date: customer.birth_date,
            notes: '',
            createdAt: new Date().toISOString().split('T')[0]
          };

          this.specialDates.push(specialDate);
          this.toggleCustomerForm();
          this.loading = false;
          console.log('Customer added to special dates:', specialDate);
        },
        error: (error) => {
          this.error = 'Failed to create customer';
          this.loading = false;
          console.error('Error creating customer:', error);
          console.error('Error details:', error.error);
        }
      });
    }
  }

  isValidCustomerForm(): boolean {
    return !!(this.newCustomer.customerName && this.newCustomer.phone && this.newCustomer.birthDate);
  }

  // Send Wish to All Upcoming Special Dates
  sendWishToAll(): void {
    const upcomingDates = this.getUpcomingDates();
    if (upcomingDates.length === 0) {
      alert('No upcoming special dates to send wishes to.');
      return;
    }

    const confirmMessage = `Send wishes to all ${upcomingDates.length} upcoming special dates?\n\nThis will open the Send Wish modal for each customer.`;
    if (confirm(confirmMessage)) {
      // Open Send Wish modal for the first customer
      this.selectedCustomer = upcomingDates[0];
      this.showSendWishModal = true;
      this.resetSendWishForm();
      
      // Show info about bulk sending
      alert(`Starting bulk wish sending...\n\nYou can now send wishes to ${upcomingDates[0].customerName}.\n\nAfter sending, you can continue with the next customer manually.`);
    }
  }
}
