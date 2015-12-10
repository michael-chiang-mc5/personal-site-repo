from django.db import models
import ast


# Citation data from pubmed
class MCPubmedCitation(models.Model):
    title = models.TextField(blank=True,null=True)
    authors = models.TextField(blank=True,null=True)
    journal = models.TextField(blank=True,null=True)
    journalAbbreviated = models.TextField(blank=True,null=True)
    volume = models.TextField(blank=True,null=True)
    number = models.TextField(blank=True,null=True)
    pages = models.TextField(blank=True,null=True)
    pubDate = models.TextField(blank=True,null=True)
    keywords = models.TextField(blank=True,null=True)
    mesh_keywords = models.TextField(blank=True,null=True)
    abstract = models.TextField(blank=True,null=True)
    doi = models.TextField(blank=True,null=True)
    pubmedID = models.PositiveIntegerField(blank=True,null=True)

    def __str__(self):
        if self.title:
            return self.title
        else:
            return "Empty citation"

    # Parses internal data and returns a truncated author list (e.g., 'Chiang et al' )
    def get_author_list_truncated(self):
        authors = self.eval_field(self.authors)
        if len(authors) is 1: # case where there is only one author
            author = authors[0]
            return author['initials'] + ' ' + author['last_name']
        else:   # case where there are multiple authors
            return authors[0]['last_name'] + ' et al'

    # Parses internal data and returns the full author list (e.g., 'M Chiang, A Cinquin, & O. Cinquin')
    def get_author_list(self):
        authors = self.eval_field(self.authors)
        if len(authors) is 1: # case where there is only one author
            author = authors[0]
            if author['first_name'][-2] == ' ':
                full_name = author['first_name'] + '. ' + author['last_name']
            else:
                full_name = author['first_name'] + ' ' + author['last_name']
            return full_name
        else:   # case where there are multiple authors TODO: implement this
            rn = ''
            for author in authors[:-1]:
                if author['first_name'][-2] == ' ':
                    rn += author['first_name'] + '. ' + author['last_name']
                else:
                    rn += author['first_name'] + ' ' + author['last_name']
                rn += ", "
            # last name is special case
            rn += "and "
            author = authors[-1]
            if author['first_name'][-2] == ' ':
                rn += author['first_name'] + '. ' + author['last_name']
            else:
                rn += author['first_name'] + ' ' + author['last_name']
            rn += '.'
            return rn

    # Returns full bibliographic source
    def get_source(self):
        source = "<i>" + self.journal +"</i>"
        if not self.is_empty_field(self.volume):
            source += ' ' + self.volume
        if not self.is_empty_field(self.number):
            source += ", no. " + self.number
        source += " (" + self.get_year_published() + ')'
        if not self.is_empty_field(self.pages):
            source += ": " + self.pages
        source += "."
        return source

    # Returns journal name
    def get_journal(self):
        return self.journal

    # Returns year article was published
    def get_year_published(self):
        date_dict = self.eval_field(self.pubDate)
        try:
            year = date_dict['Year']
        except:
             year = date_dict['MedlineDate']
        return year

    # Returns True if a saved MCPubmedCitation object with the same pubmedID exists
    # Returns False if no savved object exists
    def preExistingCitationExists(self):
        my_pk = self.eval_field(self.pubmedID)
        try:
            citation = MCPubmedCitation.objects.get(pubmedID=my_pk)
        except:
            return False
        else:
            return True

    # Returns pk of preexisting Citation object
    def preExistingCitationPk(self):
        my_pk = self.eval_field(self.pubmedID)
        citation = MCPubmedCitation.objects.get(pubmedID=my_pk)
        return citation.pk

    # saves object if it does not already exist in database (based on pubmed ID)
    # also creates associated threads and posts
    # returns pk of self, or of matching db entry
    def save_if_unique(self):
        if self.preExistingCitationExists():
            pk = self.preExistingCitationPk()
            return pk
        else:
            self.save()
            return self.pk

    # Serializes internal data into a string
    def serialize(self):
        d = self.__dict__
        d.pop("_state", None)
        return str(d)

    # Deserializes string into internal data
    def deserialize(self,str):
        d = ast.literal_eval(str)
        for key in d.keys():
            if key == 'id' or key == 'pk' or key == '_state':
                continue
            setattr(self,key,d[key])

    # parses a json string from pubmed into self
    def parse_pubmedJson(self,json_object):
        parsed_data = self.pubmedJson_to_dict(json_object)

        fieldnames = list(self.__dict__.keys())
        for fieldname in fieldnames:
            try:
                setattr(self,fieldname,parsed_data[fieldname])
            except:
                pass

    def pubmedJson_to_dict(self,json_object):
        parsed_data = dict()
        # There is no try/except because we want to be sure we are working with a proper pubmed json object
        medline_data = json_object['MedlineCitation']
        parsed_data['pubmedID'] = medline_data['PMID']
        citation_data = medline_data['Article']
        # Try to parse citation fields. Sometimes, fields will be empty (hence try/except)
        try:
            parsed_data['keywords'] = medline_data['KeywordList']
        except:
            pass
        try:
            parsed_data['mesh_keywords'] = medline_data['MeshHeadingList']['MeshHeading']
        except:
            pass
        try:
            parsed_data['PublicationType'] = citation_data['PublicationTypeList']['PublicationType']
        except:
            pass
        try:
            parsed_data['doi'] = citation_data['ELocationID']
        except:
            pass
        try:
            parsed_data['abstract'] = citation_data['Abstract']['AbstractText']
        except:
            pass
        try:
            parsed_data['pages'] = citation_data['Pagination']['MedlinePgn']
        except:
            pass
        try:
            parsed_data['number'] = citation_data['Journal']['JournalIssue']['Issue']
        except:
            pass
        try:
            parsed_data['volume'] = citation_data['Journal']['JournalIssue']['Volume']
        except:
            pass
        try:
            parsed_data['pubDate'] = citation_data['Journal']['JournalIssue']['PubDate']
        except:
            pass
        try:
            parsed_data['journal'] = citation_data['Journal']['Title']
        except:
            pass
        try:
            parsed_data['journalAbbreviated'] = citation_data['Journal']['ISOAbbreviation']
        except:
            pass
        try:
            parsed_data['title'] = citation_data['ArticleTitle']
        except:
            pass
        authors = citation_data['AuthorList']['Author']
        parsed_author_data = []
        try: # case with only one author
            single_author = dict()
            single_author['first_name'] = authors['ForeName'] # this includes middle initial
            single_author['initials'] = authors['Initials'] # this includes middle initial
            single_author['last_name'] = authors['LastName']
            parsed_author_data.append(single_author)
            parsed_data['authors'] = parsed_author_data
        except: # case with more than one author
            for author in authors:
                try: # sometimes author list contains groups like {'CollectiveName': 'Italian Pediatric TB Study Group'}. In this case, skip
                    single_author = dict()
                    single_author['first_name'] = author['ForeName'] # this includes middle initial
                    single_author['initials'] = author['Initials'] # this includes middle initial
                    single_author['last_name'] = author['LastName']
                    parsed_author_data.append(single_author)
                except:
                    pass
            parsed_data['authors'] = parsed_author_data
        return parsed_data

    # Helper function
    def eval_field(self,field):
        try:
            rn = ast.literal_eval(field)
        except:
            rn = field
        return rn

    # Helper function
    def is_empty_field(self,field):
        if not field: # check if NoneType
            return True
        if len(field)==0: # entry is ''
            return True
        return False
