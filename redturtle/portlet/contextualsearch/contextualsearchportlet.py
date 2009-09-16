from zope.interface import implements

from plone.portlets.interfaces import IPortletDataProvider
from plone.app.portlets.portlets.search import ISearchPortlet,Renderer as baseRenderer,AddForm as BaseAddForm,EditForm as BaseEditForm
from plone.app.portlets.portlets import base

from zope import schema
from zope.formlib import form
from Products.Five.browser.pagetemplatefile import ViewPageTemplateFile

from redturtle.portlet.contextualsearch import ContextualSearchPortletMessageFactory as _


from zope.component import getMultiAdapter

from Acquisition import aq_inner

class IContextualSearchPortlet(ISearchPortlet):
    """A portlet that allows contextual search and extend search portlet base
    """
    portletTitle = schema.TextLine(title=_(u"Portlet title"),
                                   description=_(u"Insert the portlet title"),
                                   required=False)
    enableContextualsearch = schema.Bool(title=_(u"Enable Contextual Search"),
                                         description=_(u"Enables the Contextual search, which shows only results from the current position"),
                                         default = False,
                                         required = False)
    
    showAdvanced = schema.Bool(title=_(u"Show advanced Search"),
                               description = _(u"Enables the advanced search link"),
                               default = False,
                               required = False)

class Assignment(base.Assignment):
    """Portlet assignment.

    This is what is actually managed through the portlets UI and associated
    with columns.
    """

    implements(IContextualSearchPortlet)

    def __init__(self,portletTitle='', enableLivesearch=True,enableContextualsearch=False,showAdvanced=False):
        self.enableLivesearch=enableLivesearch
        self.portletTitle = portletTitle
        self.enableContextualsearch = enableContextualsearch
        self.showAdvanced = showAdvanced

    @property
    def title(self):
    
        return "Contextual Search Portlet"


class Renderer(baseRenderer):
    """Portlet renderer."""


    render = ViewPageTemplateFile('contextualsearchportlet.pt')
    
    def search_action(self):
        """call the search view"""
        return '%s/contextual_search' % self.portal_url
    
    def getPosition(self):
        """returns the actual position for the contextual search"""
        plone_view = getMultiAdapter((aq_inner(self.context), self.request), name='plone')
        if plone_view.isDefaultPageInFolder():
            return '/'.join(plone_view.getParentObject().getPhysicalPath())
        else:
            return '/'.join(self.context.getPhysicalPath())
    
    def enable_advanced(self):
        """return the flag of advanced search"""
        return self.data.showAdvanced
    
    def getPortletTitle(self):
        """return the portlet title"""
        if self.data.portletTitle:
            return self.data.portletTitle
        else:
            return "search"

class AddForm(BaseAddForm):
    """Portlet add form.

    This is registered in configure.zcml. The form_fields variable tells
    zope.formlib which fields to display. The create() method actually
    constructs the assignment that is being added.
    """
    form_fields = form.Fields(IContextualSearchPortlet)

    def create(self, data):
        return Assignment(**data)


class EditForm(BaseEditForm):
    """Portlet edit form.

    This is registered with configure.zcml. The form_fields variable tells
    zope.formlib which fields to display.
    """
    form_fields = form.Fields(IContextualSearchPortlet)
