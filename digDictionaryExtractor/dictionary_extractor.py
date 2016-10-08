# -*- coding: utf-8 -*-
"""Module for defining an extractor that accepts a list of tokens
and outputs tokens that exist in a user provided trie"""
import copy

from itertools import ifilter
from pygtrie import CharTrie
from digExtractor.extractor import Extractor


class DictionaryExtractor(Extractor):

    def __init__(self):
        self.renamed_input_fields = 'tokens'
        self.pre_process = lambda x: x
        self.pre_filter = lambda x: x
        self.post_filter = lambda x: isinstance(x, basestring)
        self.trie = None
        self.metadata = {}

    def get_trie(self):
        return self.trie

    def set_trie(self, trie):
        if not isinstance(trie, CharTrie):
            raise ValueError("trie must be a CharTrie")
        self.trie = trie
        return self

    def set_pre_process(self, pre_process):
        self.pre_process = pre_process
        return self

    def set_pre_filter(self, pre_filter):
        self.pre_filter = pre_filter
        return self

    def set_post_filter(self, post_filter):
        self.post_filter = post_filter
        return self

    def extract(self, doc):
        try:
            extracts = list()
            tokens = doc['tokens']

            extracts.extend(ifilter(self.post_filter,
                                    map(self.trie.get,
                                        ifilter(self.pre_filter,
                                                map(self.pre_process, iter(tokens))))))
            return list(frozenset(extracts))

        except:
            return list()

    def get_metadata(self):
        """Returns a copy of the metadata that characterizes this extractor"""
        return copy.copy(self.metadata)

    def set_metadata(self, metadata):
        """Overwrite the metadata that characterizes this extractor"""
        self.metadata = metadata
        return self

    def get_renamed_input_fields(self):
        """Return a scalar or ordered list of fields to rename to"""
        return self.renamed_input_fields
