"""
Custom MessageBox component for PhoneBook Application
"""

import tkinter as tk
from tkinter import messagebox


def show_info(title, message):
    """Show info message"""
    messagebox.showinfo(title, message)


def show_error(title, message):
    """Show error message"""
    messagebox.showerror(title, message)


def show_success(message):
    """Show success message"""
    messagebox.showinfo("Thành công", message)


def show_warning(title, message):
    """Show warning message"""
    messagebox.showwarning(title, message)


def ask_yes_no(title, message):
    """Ask yes/no question"""
    return messagebox.askyesno(title, message)


def ask_ok_cancel(title, message):
    """Ask OK/Cancel question"""
    return messagebox.askokcancel(title, message)
