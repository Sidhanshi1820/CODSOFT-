class ContactManager:
    """A simple contact management system"""
    
    def __init__(self):
        self.contacts = []
    
    def add_contact(self):
        """Add a new contact"""
        print("\n" + "="*50)
        print("           ADD NEW CONTACT")
        print("="*50)
        
        try:
            name = input("Enter contact name: ").strip()
            if not name:
                print("Error: Name cannot be empty!")
                return
            
            phone = input("Enter phone number: ").strip()
            if not phone:
                print("Error: Phone number cannot be empty!")
                return
            
            email = input("Enter email address: ").strip()
            address = input("Enter address: ").strip()
            
            # Check if contact already exists
            for contact in self.contacts:
                if contact['name'].lower() == name.lower() or contact['phone'] == phone:
                    print("Error: Contact with this name or phone number already exists!")
                    return
            
            # Create new contact
            new_contact = {
                'name': name,
                'phone': phone,
                'email': email,
                'address': address
            }
            
            self.contacts.append(new_contact)
            print(f"\n✓ Contact '{name}' added successfully!")
            
        except Exception as e:
            print(f"Error adding contact: {e}")
    
    def view_contacts(self):
        """Display all contacts"""
        print("\n" + "="*60)
        print("CONTACT LIST")
        print("="*60)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        print(f"{'No.':<3} {'Name':<20} {'Phone':<15} {'Email':<25}")
        print("-" * 63)
        
        for i, contact in enumerate(self.contacts, 1):
            print(f"{i:<3} {contact['name']:<20} {contact['phone']:<15} {contact['email']:<25}")
    
    def search_contact(self):
        """Search for contacts by name or phone number"""
        print("\n" + "="*50)
        print("           SEARCH CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        search_term = input("Enter name or phone number to search: ").strip().lower()
        if not search_term:
            print("Error: Search term cannot be empty!")
            return
        
        found_contacts = []
        for contact in self.contacts:
            if (search_term in contact['name'].lower() or 
                search_term in contact['phone']):
                found_contacts.append(contact)
        
        if found_contacts:
            print(f"\nFound {len(found_contacts)} contact(s):")
            print("-" * 60)
            for contact in found_contacts:
                self.display_contact_details(contact)
        else:
            print("No contacts found matching your search.")
    
    def display_contact_details(self, contact):
        """Display detailed contact information"""
        print(f"Name: {contact['name']}")
        print(f"Phone: {contact['phone']}")
        print(f"Email: {contact['email']}")
        print(f"Address: {contact['address']}")
        print("-" * 40)
    
    def update_contact(self):
        """Update an existing contact"""
        print("\n" + "="*50)
        print("           UPDATE CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        self.view_contacts()
        
        try:
            choice = int(input("\nEnter contact number to update: "))
            if 1 <= choice <= len(self.contacts):
                contact = self.contacts[choice - 1]
                
                print(f"\nUpdating contact: {contact['name']}")
                print("Press Enter to keep current value:")
                
                # Update fields
                new_name = input(f"Name ({contact['name']}): ").strip()
                if new_name:
                    contact['name'] = new_name
                
                new_phone = input(f"Phone ({contact['phone']}): ").strip()
                if new_phone:
                    contact['phone'] = new_phone
                
                new_email = input(f"Email ({contact['email']}): ").strip()
                if new_email:
                    contact['email'] = new_email
                
                new_address = input(f"Address ({contact['address']}): ").strip()
                if new_address:
                    contact['address'] = new_address
                
                print(f"\n✓ Contact '{contact['name']}' updated successfully!")
                
            else:
                print("Error: Invalid contact number!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"Error updating contact: {e}")
    
    def delete_contact(self):
        """Delete a contact"""
        print("\n" + "="*50)
        print("           DELETE CONTACT")
        print("="*50)
        
        if not self.contacts:
            print("No contacts found. Please add some contacts first.")
            return
        
        self.view_contacts()
        
        try:
            choice = int(input("\nEnter contact number to delete: "))
            if 1 <= choice <= len(self.contacts):
                contact = self.contacts[choice - 1]
                
                confirm = input(f"Are you sure you want to delete '{contact['name']}'? (y/n): ").lower()
                if confirm == 'y' or confirm == 'yes':
                    deleted_contact = self.contacts.pop(choice - 1)
                    print(f"\n✓ Contact '{deleted_contact['name']}' deleted successfully!")
                else:
                    print("Delete operation cancelled.")
            else:
                print("Error: Invalid contact number!")
                
        except ValueError:
            print("Error: Please enter a valid number!")
        except Exception as e:
            print(f"Error deleting contact: {e}")
    
    def display_menu(self):
        """Display the main menu"""
        print("\n" + "="*50)
        print("           CONTACT MANAGER")
        print("="*50)
        print("1. Add Contact")
        print("2. View All Contacts")
        print("3. Search Contact")
        print("4. Update Contact")
        print("5. Delete Contact")
        print("6. Exit")
        print("="*50)
    
    def run(self):
        """Main program loop"""
        print("Welcome to Contact Manager!")
        
        while True:
            self.display_menu()
            
            try:
                choice = input("Enter your choice (1-6): ").strip()
                
                if choice == '1':
                    self.add_contact()
                elif choice == '2':
                    self.view_contacts()
                elif choice == '3':
                    self.search_contact()
                elif choice == '4':
                    self.update_contact()
                elif choice == '5':
                    self.delete_contact()
                elif choice == '6':
                    print("\nThank you for using Contact Manager!")
                    print("Goodbye!")
                    break
                else:
                    print("Error: Invalid choice! Please select 1-6.")
                
                # Pause before showing menu again
                if choice != '6':
                    input("\nPress Enter to continue...")
                    
            except KeyboardInterrupt:
                print("\n\nProgram interrupted. Goodbye!")
                break
            except Exception as e:
                print(f"An error occurred: {e}")

# Run the Contact Manager
if __name__ == "__main__":
    contact_manager = ContactManager()
    contact_manager.run()