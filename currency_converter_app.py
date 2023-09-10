"""Currency converter app

It allows the user to enter an amount and converts that amount to different
currency types

Supported types are: RON, EUR, USD, GBP
"""

import tkinter as tk
import requests
from bs4 import BeautifulSoup

__author__ = 'Marius Ciurea'
__maintainer__ = 'Marius Ciurea'

__all__ = ['CurrencyGUI']


class _GetCurrency:
    """GetCurrency class

        Attributes: url (https://cursbnr.ro/)
                    soup (BeautifulSoup object) - parse the HTML code from cursbnr.ro
        Modules: get_currency()
    """

    def __init__(self):
        self.url = 'https://cursbnr.ro/'
        response = requests.get(self.url)
        self.soup = BeautifulSoup(response.content, 'lxml')

    def get_currency(self):
        """Return a dictionary with the currencies

        Their values are reported in RON
        """

        currency = {}
        table_currencies = self.soup.find('div', {'class': 'table-responsive'})
        for tr in table_currencies.find_all('tr'):
            td = tr.find_all('td')
            if td:
                currency[td[0].text] = float(td[2].text)
        return currency


class CurrencyGUI:
    """GUI interface
        It has labels with the currency name and text boxes where
        users can enter the amount to be exchanged.
    """
    rate = _GetCurrency().get_currency()

    def __init__(self):
        self.root = tk.Tk()
        self.root.title('Currency Converter')
        self.root.geometry('350x170')
        self.root.resizable(False, False)

        self.root.configure(bg='black')

        self.main_frame = tk.Frame(self.root, width=500, height=300, bg='black')
        self.main_frame.grid(row=0, column=0)

        self.ron_label = tk.Label(self.main_frame, text='RON', font=('Arial', 16),
                                  foreground='white',
                                  bg='black')
        self.ron_label.grid(row=1, column=1, padx=5, pady=5)

        self.eur_label = tk.Label(self.main_frame, text='EUR', font=('Arial', 16),
                                  foreground='white',
                                  bg='black')
        self.eur_label.grid(row=2, column=1, padx=5, pady=5)

        self.dol_label = tk.Label(self.main_frame, text='USD', font=('Arial', 16),
                                  foreground='white',
                                  bg='black')
        self.dol_label.grid(row=3, column=1, padx=5, pady=5)

        self.gbp_label = tk.Label(self.main_frame, text='GBP', font=('Arial', 16),
                                  foreground='white',
                                  bg='black')
        self.gbp_label.grid(row=4, column=1, padx=5, pady=5)

        self.ron_text = tk.Entry(self.main_frame, font=('Arial', 16))
        self.eur_text = tk.Entry(self.main_frame, font=('Arial', 16))
        self.dol_text = tk.Entry(self.main_frame, font=('Arial', 16))
        self.gbp_text = tk.Entry(self.main_frame, font=('Arial', 16))

        self.text_widgets = [self.ron_text, self.eur_text, self.dol_text, self.gbp_text]

        self.ron_text.grid(row=1, column=2)
        self.eur_text.grid(row=2, column=2)
        self.dol_text.grid(row=3, column=2)
        self.gbp_text.grid(row=4, column=2)

        self._enter_key_bind()
        self._backspace_bind()

        self.root.mainloop()

    def _enable_all(self):
        """Changes the state of all text widgets to normal"""

        for item in self.text_widgets:
            item.configure(state='normal')

    def _clear_all(self, event):
        """Delete text from all text widgets"""

        self._enable_all()
        for item in self.text_widgets:
            item.delete(0, tk.END)

    def _backspace_bind(self):
        """Bind _clear_all function to all text widgets
        When press backspace key, all text widgets are enabled and text is deleted
        """

        for item in self.text_widgets:
            item.bind('<BackSpace>', self._clear_all)

    def _enter_key_bind(self):
        """Call the _convert method when Enter key is pressed"""

        for item in self.text_widgets:
            item.bind('<Return>', self._convert)

    @staticmethod
    def _insert_values(widget, value: str):
        """Insert a text value to a specific widget"""

        widget.insert(0, value)
        widget.configure(state='disabled')

    def _convert(self, event):
        """Convert the amount within the text box

            Supported currencies: RON, EUR, USD, GBP"""

        text_values = [widget.get() for widget in self.text_widgets]

        if text_values[0]:
            self._insert_values(self.eur_text, str(float(text_values[0])/self.rate.get('EUR')))
            self._insert_values(self.dol_text, str(float(text_values[0])/self.rate.get('USD')))
            self._insert_values(self.gbp_text, str(float(text_values[0])/self.rate.get('GBP')))

        if text_values[1]:
            self._insert_values(self.ron_text, str(float(text_values[1]) * self.rate.get('EUR')))
            self._insert_values(self.dol_text,
                                str(float(text_values[1]) * (self.rate.get('EUR') / self.rate.get('USD'))))
            self._insert_values(self.gbp_text,
                                str(float(text_values[1]) * (self.rate.get('EUR') / self.rate.get('GBP'))))

        if text_values[2]:
            self._insert_values(self.ron_text, str(float(text_values[2]) * self.rate.get('USD')))
            self._insert_values(self.eur_text,
                                str(float(text_values[2]) * (self.rate.get('USD') / self.rate.get('EUR'))))
            self._insert_values(self.gbp_text,
                                str(float(text_values[2]) * (self.rate.get('USD') / self.rate.get('GBP'))))

        if text_values[3]:
            self._insert_values(self.ron_text, str(float(text_values[3]) * self.rate.get('GBP')))
            self._insert_values(self.eur_text,
                                str(float(text_values[3]) * (self.rate.get('GBP') / self.rate.get('EUR'))))
            self._insert_values(self.dol_text,
                                str(float(text_values[3]) * (self.rate.get('GBP') / self.rate.get('USD'))))


if __name__ == '__main__':
    CurrencyGUI()
