"""Enums"""
from enum import Enum


class Binding(str, Enum):
    PAPERBACK = "paperback"
    HARDCOVER = "hardcover"
    HARDCOVER_WITH = "hard with"
    MASS_MARKET_PAPERBACK = "mass market paperback"
    OTHER = "other"




class Category(str, Enum):
    """['Accesories', 'Art', 'Audio CD', 'Biography', 'Business', 'Childrens', 'Classics', 'Contemporary', 'Crime', 'Dictionary', 'Education', 'Fantasy', 'Feminism' 'Fiction', 'Food & Drink', 'Graphic Novel', 'Health & Fitness', 'History', 'Hobby', 'Horror', 'Humour & Comedy', 'Law & Economy', 'LGBT', 'Magazines' , 'Music', 'Mystery', 'Nonfiction', 'Philosophy', 'Poetry', 'Polish Interest', 'Psychology', 'Religion', 'Romance', 'Science', 'Science-Fiction', 'Self Help', 'Sociology' 'Sport', 'Thriller', 'Travel', 'Young Adult']
    """
    ACCESSORIES = "Accessories"
    ART = "Art"
    AUDIO_CD = "Audio CD"
    BIOGRAPHY = "Biography"
    BUSINESS = "Business"
    CHILDRENS = "Childrens"
    CLASSICS = "Classics"
    CONTEMPORARY = "Contemporary"
    CRIME = "Crime"
    DICTIONARY = "Dictionary"
    EDUCATION = "Education"
    FANTASY = "Fantasy"
    FEMINISM = "Feminism"
    FICTION = "Fiction"
    FOOD_DRINK = "Food & Drink"
    GRAPHIC_NOVEL = "Graphic Novel"
    HEALTH_FITNESS = "Health & Fitness"
    HISTORY = "History"
    HOBBY = "Hobby"
    HORROR = "Horror"
    HUMOUR_COMEDY = "Humour & Comedy"
    LAW_ECONOMY = "Law & Economy"
    LGBT = "LGBT"
    MAGAZINES = "Magazines"
    MUSIC = "Music"
    MYSTERY = "Mystery"
    NONFICTION = "Nonfiction"
    PHILOSOPHY = "Philosophy"
    POETRY = "Poetry"
    POLISH_INTEREST = "Polish Interest"
    PSYCHOLOGY = "Psychology"
    RELIGION = "Religion"
    ROMANCE = "Romance"
    SCIENCE = "Science"
    SCIENCE_FICTION = "Science-Fiction"
    SELF_HELP = "Self Help"
    SOCIOLOGY = "Sociology"
    SPORT = "Sport"
    THRILLER = "Thriller"
    TRAVEL = "Travel"
    YOUNG_ADULT = "Young Adult"
    OTHER = "Other"