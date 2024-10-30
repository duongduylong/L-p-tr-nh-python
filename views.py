from flet import *
from pages.other_pages.other_report_pages.report_annual_expense import (
    Report_During_The_Year_Expense,
)
from pages.other_pages.other_report_pages.report_annual_income import (
    Report_During_The_Year_Income,
)

from pages.outcome import Outcome
from pages.income import Income
from pages.calendar import Calendar
from pages.reports.report_outcome import Report_Outcome
from pages.reports.report_income import Report_Income
from pages.other import Other
from pages.other_pages.other_report_pages.report_year_outcome import Report_Year_Outcome
from pages.other_pages.other_report_pages.report_year_income import Report_Year_Income
from pages.other_pages.other_report_pages.report_all_time import Report_All_Time
from pages.other_pages.other_report_pages.report_outcome_category_all_time import (
    Report_Outcome_Category_All_Time,
)
from pages.other_pages.other_report_pages.report_income_category_all_time import (
    Report_Income_Category_All_Time,
)
from pages.other_pages.settings import Settings
from pages.other_pages.export_data import Exportdata
from pages.search import Search


def views_handler(page):
    return {
        "/": View(
            route="/", 
            controls=[Outcome(page)]
        ),
        "/income": View(
            route="/income", 
            controls=[Income(page)]
        ),
        "/calendar": View(
            route="/calendar", 
            controls=[Calendar(page)]
        ),
        "/report_outcome": View(
            route="/report_outcome", 
            controls=[Report_Outcome(page)]
        ),
        "/report_income": View(
            route="/report_income", 
            controls=[Report_Income(page)]
        ),
        "/other": View(
            route="/other", 
            controls=[Other(page)]
        ),
        "/report_year_outcome": View(
            route="/report_year_outcome", 
            controls=[Report_Year_Outcome(page)]
        ),
        "/report_year_income": View(
            route="/report_year_income", 
            controls=[Report_Year_Income(page)]
        ),
        "/report_all_time": View(
            route="/report_all_time", 
            controls=[Report_All_Time(page)]
        ),
        "/report_outcome_category_all_time": View(
            route="/report_outcome_category_all_time",
            controls=[Report_Outcome_Category_All_Time(page)],
        ),
        "/report_income_category_all_time": View(
            route="/report_income_category_all_time",
            controls=[Report_Income_Category_All_Time(page)],
        ),
        "/report_annual_expense": View(
            route="/report_annual_expense",
            controls=[Report_During_The_Year_Expense(page)],
        ),
        "/report_annual_income": View(
            route="/report_annual_income",
            controls=[Report_During_The_Year_Income(page)],
        ),
        "/settings": View(
            route="/settings", 
            controls=[Settings(page)]
        ),
        "/export_data": View(
            route="/export_data", 
            controls=[Exportdata(page)]
        ),
        "/search": View(
            route="/search", 
            controls=[Search(page)]
        ),
    }
