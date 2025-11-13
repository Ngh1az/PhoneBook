# Testing Document - PhoneBook Application

**Project Name:** PhoneBook Application  
**Version:** 1.0  
**Date:** November 8, 2025  
**Tested By:** QA Team - Group 10

---

## Table of Contents

1. [Introduction](#introduction)
2. [Test Environment](#test-environment)
3. [Test Cases](#test-cases)
   - [Authentication](#1-authentication)
   - [Contact Management](#2-contact-management)
   - [Group Management](#3-group-management)
   - [Tag Management](#4-tag-management)
   - [Trash Management](#5-trash-management)
   - [Profile Management](#6-profile-management)
   - [Import/Export](#7-importexport)
4. [Test Results Summary](#test-results-summary)

---

## Test Cases

### 1. Authentication

#### 1.1 Login Module

| TC ID | Test Case                    | Test Steps                                                                                          | Input Data                                | Expected Result                                           |
| ----- | ---------------------------- | --------------------------------------------------------------------------------------------------- | ----------------------------------------- | --------------------------------------------------------- |
| TC01  | Login with valid credentials | 1. Navigate to login page<br>2. Enter valid username & password<br>3. Click 'Login'                 | Username: admin<br>Password: 123456       | User logs in successfully and is redirected to dashboard. |
| TC02  | Login with invalid username  | 1. Navigate to login page<br>2. Enter invalid username and valid password<br>3. Click 'Login'       | Username: invaliduser<br>Password: 123456 | Error message appears: "Username does not exist."         |
| TC03  | Login with invalid password  | 1. Navigate to login page<br>2. Enter valid username and wrong password<br>3. Click 'Login'         | Username: admin<br>Password: wrongpass    | Error message appears: "Incorrect password."              |
| TC04  | Login with empty username    | 1. Navigate to login page<br>2. Leave username field empty<br>3. Enter password<br>4. Click 'Login' | Username: (empty)<br>Password: 123456     | Error message appears: "Username is required."            |
| TC05  | Login with empty password    | 1. Navigate to login page<br>2. Enter username<br>3. Leave password field empty<br>4. Click 'Login' | Username: admin<br>Password: (empty)      | Error message appears: "Password is required."            |
| TC06  | Login with both fields empty | 1. Navigate to login page<br>2. Leave both fields empty<br>3. Click 'Login'                         | Username: (empty)<br>Password: (empty)    | Error message appears: "Username is required."            |

#### 1.2 Register Module

| TC ID | Test Case                             | Test Steps                                                                                                                   | Input Data                                                                                                                                                            | Expected Result                                                                                        |
| ----- | ------------------------------------- | ---------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------ |
| TC07  | Register with valid data              | 1. Navigate to register page<br>2. Fill all required fields with valid data<br>3. Click 'Register'                           | Full Name: John Doe<br>Username: student01<br>Email: john@gmail.com<br>Password: 123456<br>Confirm Password: 123456                                                   | Registration completes successfully; user is redirected to login page with success message.            |
| TC08  | Register with empty full name         | 1. Navigate to register page<br>2. Leave full name field empty<br>3. Fill other fields<br>4. Click 'Register'                | Full Name: (empty)<br>Username: student01<br>Email: john@gmail.com<br>Password: 123456                                                                                | Error message appears: "Full name is required."                                                        |
| TC09  | Register with empty username          | 1. Navigate to register page<br>2. Leave username field empty<br>3. Fill other fields<br>4. Click 'Register'                 | Full Name: John Doe<br>Username: (empty)<br>Email: john@gmail.com<br>Password: 123456                                                                                 | Error message appears: "Username is required."                                                         |
| TC10  | Register with empty email             | 1. Navigate to register page<br>2. Leave email field empty<br>3. Fill other fields<br>4. Click 'Register'                    | Full Name: John Doe<br>Username: student01<br>Email: (empty)<br>Password: 123456                                                                                      | Error message appears: "Email is required."                                                            |
| TC11  | Register with invalid email format    | 1. Navigate to register page<br>2. Enter invalid email format<br>3. Fill other fields<br>4. Click 'Register'                 | Full Name: John Doe<br>Username: newuser<br>Email: invalidemail<br>Password: 123456<br>Confirm Password: 123456                                                       | Error message appears: "Invalid email format."                                                         |
| TC12  | Register with existing username       | 1. Navigate to register page<br>2. Enter existing username<br>3. Fill other fields<br>4. Click 'Register'                    | Full Name: Jane Doe<br>Username: admin<br>Email: newemail@gmail.com<br>Password: 123456<br>Confirm Password: 123456                                                   | Error message appears: "Username already exists."                                                      |
| TC13  | Register with existing email          | 1. Navigate to register page<br>2. Enter existing email<br>3. Fill other fields<br>4. Click 'Register'                       | Full Name: Jane Doe<br>Username: newuser<br>Email: admin@example.com<br>Password: 123456<br>Confirm Password: 123456                                                  | Error message appears: "Email already in use."                                                         |
| TC14  | Register with short password          | 1. Navigate to register page<br>2. Enter password with less than 6 characters<br>3. Fill other fields<br>4. Click 'Register' | Full Name: John Doe<br>Username: newuser<br>Email: john@gmail.com<br>Password: 12345<br>Confirm Password: 12345                                                       | Error message appears: "Password must be at least 6 characters."                                       |
| TC15  | Register with mismatched passwords    | 1. Navigate to register page<br>2. Enter mismatched passwords<br>3. Fill other fields<br>4. Click 'Register'                 | Full Name: John Doe<br>Username: newuser<br>Email: john@gmail.com<br>Password: 123456<br>Confirm Password: 654321                                                     | Error message appears: "Password confirmation does not match."                                         |
| TC16  | Register with invalid username format | 1. Navigate to register page<br>2. Enter invalid username format<br>3. Fill other fields<br>4. Click 'Register'              | Full Name: John Doe<br>Username: user@123<br>Email: john@gmail.com<br>Password: 123456<br>Confirm Password: 123456                                                    | Error message appears: "Username can only contain letters, numbers and underscores (3-20 characters)." |
| TC17  | Register with optional fields         | 1. Navigate to register page<br>2. Fill required fields and optional fields (phone, address)<br>3. Click 'Register'          | Full Name: John Doe<br>Username: student02<br>Email: student02@gmail.com<br>Phone: 0123456789<br>Address: 123 Main St<br>Password: 123456<br>Confirm Password: 123456 | Registration completes successfully with all data saved.                                               |

#### 1.3 Logout Module

| TC ID | Test Case           | Test Steps                                                  | Input Data | Expected Result                                  |
| ----- | ------------------- | ----------------------------------------------------------- | ---------- | ------------------------------------------------ |
| TC18  | Logout successfully | 1. Login with valid credentials<br>2. Click 'Logout' button | -          | User is logged out and redirected to login page. |

---

### 2. Contact Management

#### 2.1 Add Contact

| TC ID | Test Case                               | Test Steps                                                                                                                       | Input Data                                                                                                                      | Expected Result                                               |
| ----- | --------------------------------------- | -------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------------------- | ------------------------------------------------------------- |
| TC19  | Add contact with valid data             | 1. Login successfully<br>2. Navigate to Contact page<br>3. Click 'Add Contact'<br>4. Fill all required fields<br>5. Click 'Save' | First Name: John<br>Last Name: Doe<br>Phone: 0123456789<br>Email: john@gmail.com<br>Address: 123 Main St<br>Notes: Test contact | Contact is created successfully; appears in contact list.     |
| TC20  | Add contact with empty first name       | 1. Navigate to Add Contact form<br>2. Leave first name empty<br>3. Fill other fields<br>4. Click 'Save'                          | First Name: (empty)<br>Last Name: Doe<br>Phone: 0123456789                                                                      | Error message appears: "First name is required."              |
| TC21  | Add contact with empty last name        | 1. Navigate to Add Contact form<br>2. Leave last name empty<br>3. Fill other fields<br>4. Click 'Save'                           | First Name: John<br>Last Name: (empty)<br>Phone: 0123456789                                                                     | Error message appears: "Last name is required."               |
| TC22  | Add contact with empty phone number     | 1. Navigate to Add Contact form<br>2. Leave phone number empty<br>3. Fill other fields<br>4. Click 'Save'                        | First Name: John<br>Last Name: Doe<br>Phone: (empty)                                                                            | Error message appears: "Phone number is required."            |
| TC23  | Add contact with invalid phone format   | 1. Navigate to Add Contact form<br>2. Enter invalid phone format<br>3. Fill other fields<br>4. Click 'Save'                      | First Name: John<br>Last Name: Doe<br>Phone: 123                                                                                | Error message appears: "Invalid phone number (10-11 digits)." |
| TC24  | Add contact with invalid email format   | 1. Navigate to Add Contact form<br>2. Enter invalid email format<br>3. Fill other fields<br>4. Click 'Save'                      | First Name: John<br>Last Name: Doe<br>Phone: 0123456789<br>Email: invalidemail                                                  | Error message appears: "Invalid email format."                |
| TC25  | Add contact with duplicate phone number | 1. Navigate to Add Contact form<br>2. Enter duplicate phone number<br>3. Fill other fields<br>4. Click 'Save'                    | First Name: Jane<br>Last Name: Smith<br>Phone: 0123456789<br>(existing phone)                                                   | Error message appears: "Phone number already exists."         |
| TC26  | Add contact with group                  | 1. Navigate to Add Contact form<br>2. Fill required fields<br>3. Select a group<br>4. Click 'Save'                               | First Name: John<br>Last Name: Doe<br>Phone: 0123456789<br>Group: Family                                                        | Contact is created and assigned to the selected group.        |
| TC27  | Add contact with tags                   | 1. Navigate to Add Contact form<br>2. Fill required fields<br>3. Select multiple tags<br>4. Click 'Save'                         | First Name: John<br>Last Name: Doe<br>Phone: 0123456789<br>Tags: Important, Work                                                | Contact is created with assigned tags.                        |

#### 2.2 View Contacts

| TC ID | Test Case               | Test Steps                                                          | Input Data     | Expected Result                                                                       |
| ----- | ----------------------- | ------------------------------------------------------------------- | -------------- | ------------------------------------------------------------------------------------- |
| TC28  | View all contacts       | 1. Login successfully<br>2. Navigate to Contact page                | -              | All user's contacts are displayed in a list.                                          |
| TC29  | View contact details    | 1. Navigate to Contact page<br>2. Click on a contact                | Select contact | Full contact details are displayed (name, phone, email, address, notes, group, tags). |
| TC30  | View empty contact list | 1. Login with new user (no contacts)<br>2. Navigate to Contact page | -              | Empty state message appears: "No contacts found."                                     |

#### 2.3 Update Contact

| TC ID | Test Case                            | Test Steps                                                                                                                    | Input Data                                                      | Expected Result                                                         |
| ----- | ------------------------------------ | ----------------------------------------------------------------------------------------------------------------------------- | --------------------------------------------------------------- | ----------------------------------------------------------------------- |
| TC31  | Update contact with valid data       | 1. Login successfully<br>2. Select an existing contact<br>3. Click 'Edit'<br>4. Update contact information<br>5. Click 'Save' | First Name: John Updated<br>Last Name: Doe<br>Phone: 0987654321 | Contact is updated successfully; changes are reflected in contact list. |
| TC32  | Update contact with empty first name | 1. Select an existing contact<br>2. Click 'Edit'<br>3. Clear first name field<br>4. Click 'Save'                              | First Name: (empty)<br>Last Name: Doe<br>Phone: 0123456789      | Error message appears: "First name is required."                        |
| TC33  | Update contact with invalid phone    | 1. Select an existing contact<br>2. Click 'Edit'<br>3. Enter invalid phone<br>4. Click 'Save'                                 | Phone: abc123                                                   | Error message appears: "Invalid phone number (10-11 digits)."           |
| TC34  | Update contact with invalid email    | 1. Select an existing contact<br>2. Click 'Edit'<br>3. Enter invalid email<br>4. Click 'Save'                                 | Email: bademail                                                 | Error message appears: "Invalid email format."                          |
| TC35  | Update contact group                 | 1. Select an existing contact<br>2. Click 'Edit'<br>3. Change group<br>4. Click 'Save'                                        | Group: Work (changed from Family)                               | Contact group is updated successfully.                                  |
| TC36  | Update contact tags                  | 1. Select an existing contact<br>2. Click 'Edit'<br>3. Add/remove tags<br>4. Click 'Save'                                     | Tags: Add "Important", Remove "Work"                            | Contact tags are updated successfully.                                  |

#### 2.4 Delete Contact (Soft Delete)

| TC ID | Test Case                | Test Steps                                                                               | Input Data           | Expected Result                                                    |
| ----- | ------------------------ | ---------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------------------ |
| TC37  | Delete single contact    | 1. Login successfully<br>2. Select a contact<br>3. Click 'Delete'<br>4. Confirm deletion | Select contact ID: 1 | Contact is moved to trash; no longer appears in main contact list. |
| TC38  | Cancel contact deletion  | 1. Select a contact<br>2. Click 'Delete'<br>3. Click 'Cancel'                            | -                    | Contact is NOT deleted; remains in contact list.                   |
| TC39  | Delete multiple contacts | 1. Select multiple contacts<br>2. Click 'Delete Selected'<br>3. Confirm deletion         | Select 3 contacts    | All selected contacts are moved to trash.                          |

#### 2.5 Search Contacts

| TC ID | Test Case               | Test Steps                                                                                                   | Input Data               | Expected Result                                               |
| ----- | ----------------------- | ------------------------------------------------------------------------------------------------------------ | ------------------------ | ------------------------------------------------------------- |
| TC40  | Search by name          | 1. Login successfully<br>2. Navigate to Contact page<br>3. Enter search term in search box<br>4. Press Enter | Search: "John"           | All contacts with "John" in first or last name are displayed. |
| TC41  | Search by phone         | 1. Navigate to Contact page<br>2. Enter phone number in search box                                           | Search: "0123456789"     | Contacts matching the phone number are displayed.             |
| TC42  | Search by email         | 1. Navigate to Contact page<br>2. Enter email in search box                                                  | Search: "john@gmail.com" | Contacts matching the email are displayed.                    |
| TC43  | Search with no results  | 1. Navigate to Contact page<br>2. Enter non-existing search term                                             | Search: "NonExistent"    | "No contacts found" message appears.                          |
| TC44  | Search with empty field | 1. Navigate to Contact page<br>2. Leave search field empty<br>3. Press Enter                                 | Search: (empty)          | All contacts are displayed.                                   |
| TC45  | Clear search            | 1. Perform a search<br>2. Click 'Clear' or delete search text                                                | -                        | All contacts are displayed again.                             |

#### 2.6 Filter Contacts

| TC ID | Test Case            | Test Steps                                                                          | Input Data     | Expected Result                                   |
| ----- | -------------------- | ----------------------------------------------------------------------------------- | -------------- | ------------------------------------------------- |
| TC46  | Filter by group      | 1. Navigate to Contact page<br>2. Select a group from dropdown<br>3. Click 'Filter' | Group: Family  | Only contacts in "Family" group are displayed.    |
| TC47  | Filter by tag        | 1. Navigate to Contact page<br>2. Select a tag from dropdown<br>3. Click 'Filter'   | Tag: Important | Only contacts with "Important" tag are displayed. |
| TC48  | Filter with no group | 1. Navigate to Contact page<br>2. Select "No Group" option                          | -              | Only contacts without a group are displayed.      |
| TC49  | Clear filter         | 1. Apply a filter<br>2. Click 'Clear Filter'                                        | -              | All contacts are displayed again.                 |

---

### 3. Group Management

#### 3.1 Add Group

| TC ID | Test Case                     | Test Steps                                                                                                                           | Input Data                                        | Expected Result                                       |
| ----- | ----------------------------- | ------------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------- | ----------------------------------------------------- |
| TC50  | Add group with valid data     | 1. Login successfully<br>2. Navigate to Group page<br>3. Click 'Add Group'<br>4. Enter group name and description<br>5. Click 'Save' | Group Name: Family<br>Description: Family members | Group is created successfully; appears in group list. |
| TC51  | Add group with empty name     | 1. Navigate to Add Group form<br>2. Leave group name empty<br>3. Enter description<br>4. Click 'Save'                                | Group Name: (empty)<br>Description: Test          | Error message appears: "Group name is required."      |
| TC52  | Add group without description | 1. Navigate to Add Group form<br>2. Enter group name only<br>3. Click 'Save'                                                         | Group Name: Work<br>Description: (empty)          | Group is created successfully without description.    |
| TC53  | Add duplicate group name      | 1. Navigate to Add Group form<br>2. Enter existing group name<br>3. Click 'Save'                                                     | Group Name: Family<br>(already exists)            | Error message appears: "Group name already exists."   |

#### 3.2 View Groups

| TC ID | Test Case          | Test Steps                                         | Input Data   | Expected Result                                            |
| ----- | ------------------ | -------------------------------------------------- | ------------ | ---------------------------------------------------------- |
| TC54  | View all groups    | 1. Login successfully<br>2. Navigate to Group page | -            | All user's groups are displayed with contact count.        |
| TC55  | View group details | 1. Navigate to Group page<br>2. Click on a group   | Select group | Group details and all contacts in the group are displayed. |

#### 3.3 Update Group

| TC ID | Test Case                    | Test Steps                                                                                                   | Input Data                                   | Expected Result                                  |
| ----- | ---------------------------- | ------------------------------------------------------------------------------------------------------------ | -------------------------------------------- | ------------------------------------------------ |
| TC56  | Update group name            | 1. Navigate to Group page<br>2. Select a group<br>3. Click 'Edit'<br>4. Update group name<br>5. Click 'Save' | Group Name: Friends<br>(changed from Family) | Group name is updated successfully.              |
| TC57  | Update group description     | 1. Select a group<br>2. Click 'Edit'<br>3. Update description<br>4. Click 'Save'                             | Description: Close friends only              | Group description is updated successfully.       |
| TC58  | Update group with empty name | 1. Select a group<br>2. Click 'Edit'<br>3. Clear group name<br>4. Click 'Save'                               | Group Name: (empty)                          | Error message appears: "Group name is required." |

#### 3.4 Delete Group

| TC ID | Test Case                  | Test Steps                                                                                                  | Input Data                   | Expected Result                                     |
| ----- | -------------------------- | ----------------------------------------------------------------------------------------------------------- | ---------------------------- | --------------------------------------------------- |
| TC59  | Delete empty group         | 1. Navigate to Group page<br>2. Select a group with no contacts<br>3. Click 'Delete'<br>4. Confirm deletion | Select group with 0 contacts | Group is deleted successfully.                      |
| TC60  | Delete group with contacts | 1. Select a group with contacts<br>2. Click 'Delete'<br>3. Confirm deletion                                 | Select group with contacts   | Group is deleted; contacts are moved to "No Group". |
| TC61  | Cancel group deletion      | 1. Select a group<br>2. Click 'Delete'<br>3. Click 'Cancel'                                                 | -                            | Group is NOT deleted; remains in group list.        |

---

### 4. Tag Management

#### 4.1 Add Tag

| TC ID | Test Case                   | Test Steps                                                                                                                     | Input Data                                             | Expected Result                                   |
| ----- | --------------------------- | ------------------------------------------------------------------------------------------------------------------------------ | ------------------------------------------------------ | ------------------------------------------------- |
| TC62  | Add tag with valid data     | 1. Login successfully<br>2. Navigate to Tag page<br>3. Click 'Add Tag'<br>4. Enter tag name and description<br>5. Click 'Save' | Tag Name: Important<br>Description: Important contacts | Tag is created successfully; appears in tag list. |
| TC63  | Add tag with empty name     | 1. Navigate to Add Tag form<br>2. Leave tag name empty<br>3. Click 'Save'                                                      | Tag Name: (empty)                                      | Error message appears: "Tag name is required."    |
| TC64  | Add tag without description | 1. Navigate to Add Tag form<br>2. Enter tag name only<br>3. Click 'Save'                                                       | Tag Name: Work<br>Description: (empty)                 | Tag is created successfully without description.  |
| TC65  | Add duplicate tag name      | 1. Navigate to Add Tag form<br>2. Enter existing tag name<br>3. Click 'Save'                                                   | Tag Name: Important<br>(already exists)                | Error message appears: "Tag name already exists." |

#### 4.2 View Tags

| TC ID | Test Case        | Test Steps                                       | Input Data | Expected Result                                          |
| ----- | ---------------- | ------------------------------------------------ | ---------- | -------------------------------------------------------- |
| TC66  | View all tags    | 1. Login successfully<br>2. Navigate to Tag page | -          | All user's tags are displayed with contact count.        |
| TC67  | View tag details | 1. Navigate to Tag page<br>2. Click on a tag     | Select tag | Tag details and all contacts with the tag are displayed. |

#### 4.3 Update Tag

| TC ID | Test Case                  | Test Steps                                                                                             | Input Data                                | Expected Result                                |
| ----- | -------------------------- | ------------------------------------------------------------------------------------------------------ | ----------------------------------------- | ---------------------------------------------- |
| TC68  | Update tag name            | 1. Navigate to Tag page<br>2. Select a tag<br>3. Click 'Edit'<br>4. Update tag name<br>5. Click 'Save' | Tag Name: VIP<br>(changed from Important) | Tag name is updated successfully.              |
| TC69  | Update tag description     | 1. Select a tag<br>2. Click 'Edit'<br>3. Update description<br>4. Click 'Save'                         | Description: Very important people        | Tag description is updated successfully.       |
| TC70  | Update tag with empty name | 1. Select a tag<br>2. Click 'Edit'<br>3. Clear tag name<br>4. Click 'Save'                             | Tag Name: (empty)                         | Error message appears: "Tag name is required." |

#### 4.4 Delete Tag

| TC ID | Test Case           | Test Steps                                                                             | Input Data | Expected Result                            |
| ----- | ------------------- | -------------------------------------------------------------------------------------- | ---------- | ------------------------------------------ |
| TC71  | Delete tag          | 1. Navigate to Tag page<br>2. Select a tag<br>3. Click 'Delete'<br>4. Confirm deletion | Select tag | Tag is deleted; removed from all contacts. |
| TC72  | Cancel tag deletion | 1. Select a tag<br>2. Click 'Delete'<br>3. Click 'Cancel'                              | -          | Tag is NOT deleted; remains in tag list.   |

---

### 5. Trash Management

#### 5.1 View Trash

| TC ID | Test Case             | Test Steps                                         | Input Data | Expected Result                        |
| ----- | --------------------- | -------------------------------------------------- | ---------- | -------------------------------------- |
| TC73  | View deleted contacts | 1. Login successfully<br>2. Navigate to Trash page | -          | All deleted contacts are displayed.    |
| TC74  | View empty trash      | 1. Navigate to Trash page (no deleted contacts)    | -          | "No deleted contacts" message appears. |

#### 5.2 Restore Contacts

| TC ID | Test Case                 | Test Steps                                                                              | Input Data           | Expected Result                                         |
| ----- | ------------------------- | --------------------------------------------------------------------------------------- | -------------------- | ------------------------------------------------------- |
| TC75  | Restore single contact    | 1. Navigate to Trash page<br>2. Select a deleted contact<br>3. Click 'Restore'          | Select contact ID: 1 | Contact is restored; appears back in main contact list. |
| TC76  | Restore multiple contacts | 1. Navigate to Trash page<br>2. Select multiple contacts<br>3. Click 'Restore Selected' | Select 3 contacts    | All selected contacts are restored successfully.        |
| TC77  | Cancel restore operation  | 1. Select a contact<br>2. Click 'Restore'<br>3. Click 'Cancel'                          | -                    | Contact remains in trash.                               |

#### 5.3 Permanent Delete

| TC ID | Test Case                            | Test Steps                                                                                              | Input Data           | Expected Result                                     |
| ----- | ------------------------------------ | ------------------------------------------------------------------------------------------------------- | -------------------- | --------------------------------------------------- |
| TC78  | Permanently delete single contact    | 1. Navigate to Trash page<br>2. Select a deleted contact<br>3. Click 'Delete Permanently'<br>4. Confirm | Select contact ID: 1 | Contact is permanently deleted; cannot be restored. |
| TC79  | Permanently delete multiple contacts | 1. Navigate to Trash page<br>2. Select multiple contacts<br>3. Click 'Delete Permanently'<br>4. Confirm | Select 3 contacts    | All selected contacts are permanently deleted.      |
| TC80  | Empty trash                          | 1. Navigate to Trash page<br>2. Click 'Empty Trash'<br>3. Confirm                                       | -                    | All contacts in trash are permanently deleted.      |
| TC81  | Cancel permanent deletion            | 1. Select a contact<br>2. Click 'Delete Permanently'<br>3. Click 'Cancel'                               | -                    | Contact remains in trash.                           |

---

### 6. Profile Management

#### 6.1 View Profile

| TC ID | Test Case         | Test Steps                                           | Input Data | Expected Result                                                                    |
| ----- | ----------------- | ---------------------------------------------------- | ---------- | ---------------------------------------------------------------------------------- |
| TC82  | View user profile | 1. Login successfully<br>2. Navigate to Profile page | -          | User profile information is displayed (fullname, username, email, phone, address). |

#### 6.2 Update Profile

| TC ID | Test Case                          | Test Steps                                                                                                          | Input Data                                                                                            | Expected Result                                                   |
| ----- | ---------------------------------- | ------------------------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------------- | ----------------------------------------------------------------- |
| TC83  | Update profile with valid data     | 1. Navigate to Profile page<br>2. Click 'Edit Profile'<br>3. Update profile information<br>4. Click 'Save'          | Full Name: John Doe Updated<br>Email: newemail@gmail.com<br>Phone: 0987654321<br>Address: New Address | Profile is updated successfully.                                  |
| TC84  | Update profile with empty fullname | 1. Navigate to Profile page<br>2. Click 'Edit Profile'<br>3. Clear fullname field<br>4. Click 'Save'                | Full Name: (empty)                                                                                    | Error message appears: "Full name is required."                   |
| TC85  | Update profile with invalid email  | 1. Navigate to Profile page<br>2. Click 'Edit Profile'<br>3. Enter invalid email<br>4. Click 'Save'                 | Email: invalidemail                                                                                   | Error message appears: "Invalid email format."                    |
| TC86  | Update profile with invalid phone  | 1. Navigate to Profile page<br>2. Click 'Edit Profile'<br>3. Enter invalid phone<br>4. Click 'Save'                 | Phone: 123                                                                                            | Error message appears: "Invalid phone number (10-11 digits)."     |
| TC87  | Update profile with existing email | 1. Navigate to Profile page<br>2. Click 'Edit Profile'<br>3. Enter email used by another account<br>4. Click 'Save' | Email: existing@example.com                                                                           | Error message appears: "Email already in use by another account." |

#### 6.3 Change Password

| TC ID | Test Case                                      | Test Steps                                                                                               | Input Data                                                                 | Expected Result                                                            |
| ----- | ---------------------------------------------- | -------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------- | -------------------------------------------------------------------------- |
| TC88  | Change password with valid data                | 1. Navigate to Profile page<br>2. Click 'Change Password'<br>3. Fill password fields<br>4. Click 'Save'  | Old Password: 123456<br>New Password: newpass123<br>Confirm: newpass123    | Password is changed successfully.                                          |
| TC89  | Change password with wrong old password        | 1. Navigate to Change Password<br>2. Enter wrong old password<br>3. Fill other fields<br>4. Click 'Save' | Old Password: wrongpass<br>New Password: newpass123<br>Confirm: newpass123 | Error message appears: "Current password is incorrect."                    |
| TC90  | Change password with mismatched new passwords  | 1. Navigate to Change Password<br>2. Enter mismatched new passwords<br>3. Click 'Save'                   | Old Password: 123456<br>New Password: newpass123<br>Confirm: different123  | Error message appears: "Password confirmation does not match."             |
| TC91  | Change password with short new password        | 1. Navigate to Change Password<br>2. Enter short new password<br>3. Click 'Save'                         | Old Password: 123456<br>New Password: 123<br>Confirm: 123                  | Error message appears: "Password must be at least 6 characters."           |
| TC92  | Change password with same old and new password | 1. Navigate to Change Password<br>2. Enter same password as old<br>3. Click 'Save'                       | Old Password: 123456<br>New Password: 123456<br>Confirm: 123456            | Error message appears: "New password must be different from old password." |

---

### 7. Import/Export

#### 7.1 Export Contacts

| TC ID | Test Case                  | Test Steps                                                                                    | Input Data           | Expected Result                                                       |
| ----- | -------------------------- | --------------------------------------------------------------------------------------------- | -------------------- | --------------------------------------------------------------------- |
| TC93  | Export all contacts to CSV | 1. Login successfully<br>2. Navigate to Dashboard or Contact page<br>3. Click 'Export to CSV' | -                    | CSV file is downloaded with all contacts; file contains correct data. |
| TC94  | Export filtered contacts   | 1. Apply a filter (e.g., by group)<br>2. Click 'Export to CSV'                                | Filter: Family group | CSV file contains only filtered contacts.                             |
| TC95  | Export with no contacts    | 1. Login with new user (no contacts)<br>2. Click 'Export to CSV'                              | -                    | CSV file is created with headers only (no data rows).                 |

#### 7.2 Import Contacts

| TC ID | Test Case                           | Test Steps                                                                                                                                       | Input Data                                                              | Expected Result                                                                      |
| ----- | ----------------------------------- | ------------------------------------------------------------------------------------------------------------------------------------------------ | ----------------------------------------------------------------------- | ------------------------------------------------------------------------------------ |
| TC96  | Import contacts from valid CSV      | 1. Login successfully<br>2. Navigate to Dashboard or Contact page<br>3. Click 'Import from CSV'<br>4. Select valid CSV file<br>5. Click 'Import' | CSV file with valid data<br>(first_name, last_name, phone, email, etc.) | Contacts are imported successfully; appear in contact list.                          |
| TC97  | Import with invalid CSV format      | 1. Click 'Import from CSV'<br>2. Select invalid CSV file (wrong headers)<br>3. Click 'Import'                                                    | CSV with invalid format                                                 | Error message appears: "Invalid CSV format."                                         |
| TC98  | Import with duplicate phone numbers | 1. Click 'Import from CSV'<br>2. Select CSV file with duplicate phone numbers<br>3. Click 'Import'                                               | CSV with existing phone numbers                                         | Duplicates are skipped; unique contacts are imported; summary message shows results. |
| TC99  | Import with invalid data            | 1. Click 'Import from CSV'<br>2. Select CSV with invalid email/phone<br>3. Click 'Import'                                                        | CSV with invalid data                                                   | Invalid rows are skipped; valid rows are imported; error report is shown.            |
| TC100 | Import empty CSV file               | 1. Click 'Import from CSV'<br>2. Select empty CSV file<br>3. Click 'Import'                                                                      | Empty CSV file                                                          | Error message appears: "CSV file is empty."                                          |
| TC101 | Cancel import operation             | 1. Click 'Import from CSV'<br>2. Select file<br>3. Click 'Cancel'                                                                                | -                                                                       | Import is cancelled; no contacts are imported.                                       |

---

### 8. Dashboard

#### 8.1 View Dashboard

| TC ID | Test Case                   | Test Steps                                                       | Input Data | Expected Result                                                             |
| ----- | --------------------------- | ---------------------------------------------------------------- | ---------- | --------------------------------------------------------------------------- |
| TC102 | View dashboard statistics   | 1. Login successfully<br>2. Dashboard is displayed automatically | -          | Dashboard shows: total contacts, total groups, total tags, recent contacts. |
| TC103 | View dashboard with no data | 1. Login with new user<br>2. View dashboard                      | -          | Dashboard shows zero counts; "No recent contacts" message appears.          |

#### 8.2 Quick Actions

| TC ID | Test Case                           | Test Steps                                                                                  | Input Data                                                | Expected Result                                           |
| ----- | ----------------------------------- | ------------------------------------------------------------------------------------------- | --------------------------------------------------------- | --------------------------------------------------------- |
| TC104 | Quick add contact from dashboard    | 1. Navigate to Dashboard<br>2. Click 'Quick Add Contact'<br>3. Fill form<br>4. Click 'Save' | First Name: Quick<br>Last Name: Test<br>Phone: 0111111111 | Contact is added; dashboard refreshes with updated count. |
| TC105 | Navigate to contacts from dashboard | 1. On Dashboard<br>2. Click 'View All Contacts'                                             | -                                                         | User is redirected to Contact page.                       |
| TC106 | Navigate to groups from dashboard   | 1. On Dashboard<br>2. Click 'Manage Groups'                                                 | -                                                         | User is redirected to Group page.                         |

---

### 9. Backup (Auto Backup)

| TC ID | Test Case                 | Test Steps                                                                    | Input Data | Expected Result                                        |
| ----- | ------------------------- | ----------------------------------------------------------------------------- | ---------- | ------------------------------------------------------ |
| TC107 | Automatic backup creation | 1. Login successfully<br>2. Add/update contacts<br>3. Wait for backup trigger | -          | Backup file is created automatically in backup folder. |
| TC108 | View backup files         | 1. Navigate to backup folder<br>2. Check for backup files                     | -          | Backup files exist with timestamp in filename.         |

---

### 10. Error Handling

| TC ID | Test Case                    | Test Steps                                                            | Input Data          | Expected Result                                                  |
| ----- | ---------------------------- | --------------------------------------------------------------------- | ------------------- | ---------------------------------------------------------------- |
| TC109 | Database connection error    | 1. Stop MySQL server<br>2. Try to login                               | -                   | Error message appears: "Cannot connect to database."             |
| TC110 | Invalid database credentials | 1. Modify config.py with wrong DB credentials<br>2. Start application | -                   | Error message appears: "Database connection failed."             |
| TC111 | Large file import            | 1. Try to import very large CSV file (>10MB)<br>2. Click 'Import'     | Very large CSV file | Application handles gracefully; shows progress or error message. |

---

### 11. UI/UX Testing

| TC ID | Test Case                       | Test Steps                                                                                 | Input Data | Expected Result                                                 |
| ----- | ------------------------------- | ------------------------------------------------------------------------------------------ | ---------- | --------------------------------------------------------------- |
| TC112 | Window resizing                 | 1. Open application<br>2. Resize window to smaller size                                    | -          | UI elements adjust properly; no overlapping or hidden elements. |
| TC113 | Navigation between pages        | 1. Login successfully<br>2. Navigate between different pages<br>3. Return to previous page | -          | Navigation works smoothly; data persists correctly.             |
| TC114 | Form validation visual feedback | 1. Try to submit form with invalid data                                                    | -          | Invalid fields are highlighted; clear error messages appear.    |
| TC115 | Button states                   | 1. Perform various actions<br>2. Observe button states                                     | -          | Buttons show appropriate states (enabled/disabled, loading).    |

---

## Test Results Summary

| Module             | Total Test Cases | Passed | Failed | Pass Rate |
| ------------------ | ---------------- | ------ | ------ | --------- |
| Authentication     | 18               | -      | -      | -         |
| Contact Management | 31               | -      | -      | -         |
| Group Management   | 12               | -      | -      | -         |
| Tag Management     | 11               | -      | -      | -         |
| Trash Management   | 9                | -      | -      | -         |
| Profile Management | 11               | -      | -      | -         |
| Import/Export      | 13               | -      | -      | -         |
| Dashboard          | 5                | -      | -      | -         |
| Backup             | 2                | -      | -      | -         |
| Error Handling     | 3                | -      | -      | -         |
| UI/UX              | 4                | -      | -      | -         |
| **TOTAL**          | **115**          | **-**  | **-**  | **-**     |

---

