from flask_login import UserMixin
from reflection.database import Base
from sqlalchemy import Boolean, Column, DateTime, Enum, ForeignKey, Integer, String, Table, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from uuid import uuid4

# Person-related
class Account(Base, UserMixin):
    __tablename__ = 'account'
    id = Column(Integer, primary_key=True, nullable=False)
    username = Column(String(30), unique=True, nullable=False) # usually NYU NetID
    password = Column(String(150), nullable=False)
    enabled = Column(Boolean, default=True, nullable=False)
    dir_authn = Column(Boolean, default=True, nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    person = relationship('Person', backref='account')
    sessions = relationship('Session', backref='account')
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Account {}>'.format(self.id)

    def is_active(self):
        return self.enabled

    def is_authenticated(self):
        return True

    def is_anonymous(self):
        if self.username == None:
            return False
        else:
            return True

    def get_id(self):
        return unicode(self.id)

# e.g. 'Student' or 'Faculty' and many others
class Affiliation(Base):
    __tablename__ = 'affiliation'
    id = Column(Integer, primary_key=True, nullable=False)
    affiliation = Column(String(30), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Affiliation {}>'.format(self.id)

class Person(Base):
    __tablename__ = 'person'
    id = Column(Integer, primary_key=True, nullable=False)
    official_firstname = Column(String(100), nullable=False)
    official_middlename = Column(String(100), nullable=True)
    official_lastname = Column(String(100), nullable=False)
    preferred_firstname = Column(String(100), nullable=False)
    preferred_middlename = Column(String(100), nullable=True)
    preferred_lastname = Column(String(100), nullable=False)
    gender = Column(String(5), nullable=False)
    university_n = Column(String(50), nullable=True) # NYU "N number"
    affiliations = relationship('Affiliation', backref='person', secondary='affiliation_person')
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Person {}>'.format(self.id)

class Session(Base):
    __tablename__ = 'session'
    id = Column(Integer, primary_key=True, nullable=False)
    account_id = Column(Integer, ForeignKey('account.id'), nullable=False)
    #expires_at = Column(DateTime, nullable=False)
    guid = Column(String(50), unique=True, default=str(uuid4()), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Session {}>'.format(self.id)

# Course-related
class Course(Base):
    __tablename__ = 'course'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    subject_id = Column(Integer, ForeignKey('subject.id'), nullable=False)
    subject = relationship('Subject')
    catalog_num = Column(String(25), nullable=True) # e.g. the 2001 in ITPG-GT 2001
    url = Column(String(255), nullable=True)
    description = Column(Text, nullable=False)
    #predecessor_id = Column(Integer, ForeignKey('course.id'), nullable=True)
    #predecessor = relationship('Course', backref='successors', remote_side=[id])
    visibility = Column(Enum('hidden', 'private', 'project', 'section', 'course',
                             'community', 'public', name='visibility_enum'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Course {}>'.format(self.id)

class Section(Base):
    __tablename__ = 'section'
    id = Column(Integer, primary_key=True, nullable=False)
    section_num = Column(Integer, default=1, nullable=False)
    call_num = Column(Integer, nullable=True) # will be null until registrar gives us call numbers
    course_id = Column(Integer, ForeignKey('course.id'), nullable=False)
    course = relationship('Course', backref='sections')
    term_id = Column(Integer, ForeignKey('term.id'), nullable=False)
    term = relationship('Term', backref='sections')
    enrollment_limit = Column(Integer, default=18, nullable=False)
    # enrollment # count of students in the section, potentially via dynamic lookup
    # credit # default 4, nullable?
    url = Column(String(255), nullable=True)
    instructors = relationship('Person', backref='sections', secondary='instructor_section')
    students = relationship('Person', backref='students', secondary='section_student')
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Section {}>'.format(self.id)

# Albert "subject" / "subject area" - this is a department, more or less
class Subject(Base):
    __tablename__ = 'subject'
    id = Column(Integer, primary_key=True, nullable=False)
    subject = Column(String(25), unique=True, nullable=False) # e.g. ITPG-GT
    description = Column(String(50), nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Subject {}>'.format(self.id)
    
class Term(Base):
    __tablename__ = 'term'
    id = Column(Integer, primary_key=True, nullable=False)
    term = Column(String(30), unique=True, nullable=False) # e.g. Fall 2014
    term_shortname = Column(Enum('Spring', 'Summer', 'Summer1', 'Summer2', 'Fall', name='term_shortname_enum'),
                            nullable=False)
    #term_num = Column(Integer, unique=True, nullable=False) # e.g. 20143
    term_year = Column(Integer, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Term {}>'.format(self.id)

# Project-related
class Doc(Base):
    __tablename__ = 'doc'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    path = Column(String(255), nullable=False)
    project_id = Column(Integer, ForeignKey('project.id'), nullable=False)
    project = relationship('Project', backref='docs', foreign_keys=project_id)
    visibility = Column(Enum('hidden', 'private', 'project', 'section', 'course',
                             'community', 'public', name='visibility_enum'), nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Doc {}>'.format(self.id)
    
class Project(Base):
    __tablename__ = 'project'
    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String(255), nullable=False)
    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
    persons = relationship('Person', backref='projects', secondary='person_project')
    description = Column(Text, nullable=True)
    elevator_pitch = Column(Text, nullable=True)
    url = Column(String(255), nullable=True)
    audience = Column(Text, nullable=True)
    background = Column(Text, nullable=True)
    user_scenario = Column(Text, nullable=True)
    technical_system = Column(Text, nullable=True)
    conclusion = Column(Text, nullable=True)
    research = Column(Text, nullable=True)
    personal_statement = Column(Text, nullable=True)
    # ForeignKey use_alter avoids circular dependency on Doc at table creation
    image_id = Column(Integer, ForeignKey('doc.id', use_alter=True, name='image_id_constraint'), nullable=True)
    #docs = relationship('Doc', backref='project')
    venues = relationship('Venue', backref='projects', secondary='project_venue')
    tags = relationship('Tag', backref='projects', secondary='project_tag')
    thesis = Column(Boolean, default=False, nullable=False)
    # sustain = Column(Text, nullable=True)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Project {}>'.format(self.id)

class Tag(Base):
    __tablename__ = 'tag'
    id = Column(Integer, primary_key=True, nullable=False)
    tag = Column(String(100), unique=True, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Tag {}>'.format(self.id)

class Venue(Base):
    __tablename__ = 'venue'
    id = Column(Integer, primary_key=True, nullable=False)
    venue = Column(String(255), unique=True, nullable=False)
    shortname = Column(String(10), unique=True, nullable=False)
    description = Column(Text, nullable=True)
    #venue_date        | datetime     | YES  | MUL | NULL    |                |
    term_id = Column(Integer, ForeignKey('term.id'), nullable=False)
    term = relationship('Term', backref='venues')
    active = Column(Boolean, default=True, nullable=False)
    #equipment_active = Column(Boolean, default=True, nullable=False)
    map_active = Column(Boolean, default=True, nullable=False)
    searchable = Column(Boolean, default=False, nullable=False)
    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)

    def __repr__(self):
        return '<Venue {}>'.format(self.id)

# class Applicant(Base): # from admissions process
# class CourseProposal(Base): # let's keep the course data clean, containing only the courses that actually run
# class Equipment(Base): # Clay's suggestion that the ER data should be social
# class Evaluation(Base): # course evals
# class Link(Base): # long lost link sharing
# class Post(Base): # Build your own microblog!
# class Opportunity(Base): # TAP will come back, one day
# class Provider(Base): # TAP continued
# class ThesisVideo(Base): # Shawn's video archive

# class IDCard(Base):
#    __tablename__ = 'card'
#    id = Column(Integer, primary_key=True, nullable=False)
#    serial = Column(String(30), unique=True, nullable=False)
#    person_id = Column(Integer, ForeignKey('person.id'), nullable=False)
#    enabled = Column(Boolean, default=True, nullable=False)
#    created_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
#    modified_at = Column(DateTime(timezone=True), default=func.now(), nullable=False)
#
#    def __repr__(self):
#        return '<IDCard {}>'.format(self.id)

# Association tables
affiliation_person = Table('affiliation_person', Base.metadata,
    Column('affiliation_id', Integer, ForeignKey('affiliation.id'), nullable=False),
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False))

#course_section = Table('course_section', Base.metadata,
#    Column('course_id', Integer, ForeignKey('course.id'), nullable=False),
#    Column('section_id', Integer, ForeignKey('section.id'), nullable=False))

instructor_section = Table('instructor_section', Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('section_id', Integer, ForeignKey('section.id'), nullable=False))

person_project = Table('person_project', Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('project_id', Integer, ForeignKey('project.id'), nullable=False))

project_tag = Table('project_tag', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id'), nullable=False),
    Column('tag_id', Integer, ForeignKey('tag.id'), nullable=False))

project_venue = Table('project_venue', Base.metadata,
    Column('project_id', Integer, ForeignKey('project.id'), nullable=False),
    Column('venue_id', Integer, ForeignKey('venue.id'), nullable=False))

section_student = Table('section_student', Base.metadata,
    Column('person_id', Integer, ForeignKey('person.id'), nullable=False),
    Column('section_id', Integer, ForeignKey('section.id'), nullable=False))
