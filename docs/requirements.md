# PhoneBook Application Requirements

## I. Functional Requirements

### 1. User Management

#### 1.1 User Registration

- Users can create a new account by entering: **Fullname**, **Email**, **Username**, **Password**
- The system checks for duplicate emails or usernames before saving to the database.
- Passwords are encrypted (hash) before being stored.

#### 1.2 User Login

- User logs in with username and password.
- The system verifies the information, if correct → goes to Dashboard.
- If incorrect → displays an error message.

#### 1.3 Profile Management

- Users can view and edit personal information: Full name, Email, Phone number, Address, Password.
- The new password is re-authenticated before updating.

#### 1.4 Logout

- User can log out of the system
- After logging out, return to the login interface

---

### 2. Contacts Management

#### 2.1 Add New Contact

- Users can add new contacts with the following fields:
  - Full name (First name, Last name)
  - Phone number (Phone number)
  - Email (optional)
  - Address (optional)
  - Notes (optional)
- Data is checked for validity (correct phone number and email format) before saving.

#### 2.2 View Contacts

- The system displays a list of all the user's contacts.
- Contacts can be sorted, searched, or filtered by name, group, or tag.

#### 2.3 Update Contact

- Người dùng có thể chọn một liên hệ và chỉnh sửa thông tin.
- Sau khi cập nhật, danh sách tự động hiển thị lại.

#### 2.4 Delete Contact (Soft Delete)

- When deleting a contact, the system only marks it as "deleted" (soft delete), not permanently deleting it from the database.
- Users can restore deleted contacts.

---

### 3. Trash

#### 3.1 View Deleted Contacts

- Users can open the Trash page to see a list of soft deleted contacts.
- Each entry displays: Full name, phone number, date deleted, and the option to **Restore** or **Delete Permanently**

#### 3.2 Restore Contact

- Users can select one or more contacts in the Trash to restore to the main list.
- When restoring, the "deleted" status of the contact is reset to "active".

#### 3.3 Permanently Delete Contact

- Users can select contacts in Trash and permanently delete them from the MySQL database.
- Once permanently deleted, contacts cannot be recovered.

---

### 4. Group/Tag Management

#### 4.1 Create Group/Tag

- Users can create groups or tags to categorize contacts.
- Enter a name and a short description for the group/tag.
- The system prevents duplicate names within the same account.

#### 4.2 Assign Contacts to Group/Tag

- Users can assign one or more contacts to a selected group/tag.
- A contact can belong to multiple tags but only one main group.

#### 4.3 View and Manage Group/Tag

- Users can view a list of all existing groups/tags.
- Can filter contacts by group or tag.

#### 4.4 Update Group/Tag

- Users can edit the name or description of an existing group/tag.
- System checks for duplicate names before saving changes.

#### 4.5 Delete Group/Tag

- When you delete a group/tag, the contacts in it are not lost, only the category association is lost.

---

### 5. Dashboard and Statistics

- The main screen displays the total:
  - **Total Contacts**
  - **Number of Groups**
  - **Number of Tags in Use**
- Simple figures help users grasp information quickly.

---

## II. Non-Functional Requirements

### 1. System Environment

- **Programming Language:** Python 3.10+
- **Database Management System:** MySQL 8.0+
- **GUI Framework:** Tkinter
- **Architecture:** Model–View–Controller (MVC)
- **Operating System:** Windows 10/11

### 2. Performance Requirements

- The application starts up in ≤ 5 seconds.
- The main operations (add, edit, search, login) respond in ≤ 2 seconds.
- The system handles smoothly with a minimum of 1,000 contacts without freezing.

### 3. Security Requirements

- User passwords must be encrypted with **bcrypt** before being stored in MySQL.
- The application performs input validation to avoid formatting errors.
- Each account can only access its own data.
- After the user logs out, the login session must be completely deleted from memory.

### 4. Usability Requirements

- The user interface is built with Tkinter, friendly and easy to understand.
- The entire interface is displayed in Vietnamese.
- The buttons, menus and icons are clearly labeled.
- There are notifications when the user performs a successful or failed operation.

### 5. Reliability Requirements

- When MySQL connection is lost, the system displays a warning instead of crashing the application.
- **Soft Delete** mechanism helps to avoid permanent data loss.
- Data between tables (User, Contact, Group/Tag, Trash) is guaranteed to be consistent.
- The system logs errors to the `error_log.txt` file for easy checking.

### 6. Backup and Recovery

- Users can export contact data to CSV file for manual backup.
- Data can be restored from CSV file when recovery is needed.

### 7. User Interface Requirements

- Main interface includes:
  - **Dashboard:** Displays an overview of contacts.
  - **Contacts:** Manage contacts, support searching, adding, editing, deleting, restoring (Trash).
  - **Groups/Tags:** Classify contacts.
  - **Profile:** Update personal information.
- Sidebar helps to move quickly between screens.
- Soft colors, easy-to-see layout, easy-to-read fonts

---

**Document Version:** 1.0  
**Date:** November 2, 2025  
**Project:** PhoneBook Application - Group 10
