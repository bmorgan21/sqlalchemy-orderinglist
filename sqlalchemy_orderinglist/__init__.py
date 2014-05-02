from sqlalchemy.ext.orderinglist import OrderingList, _unsugar_count_from

__all__ = ['ordering_list']

def ordering_list(attr, count_from=None, **kw):
    kw = _unsugar_count_from(count_from=count_from, **kw)

    constants = kw.pop('constants', None)
    if constants:
        return lambda: OrderingListWithConstants(constants, attr, **kw)
    else:
        return lambda: OrderingList(attr, **kw)

class OrderingListWithConstants(OrderingList):
    def __init__(self, constants, ordering_attr=None, ordering_func=None,
                 reorder_on_append=False):
        self.constants = constants
        OrderingList.__init__(self, ordering_attr=ordering_attr,
                              ordering_func=ordering_func, reorder_on_append=reorder_on_append)

    def _set_constants(self, entity):
        for k,v in self.constants.items():
            setattr(entity, k, v)

    def _unset_constants(self, entity):
        for k in self.constants.keys():
            setattr(entity, k, None)

    def append(self, entity):
        self._set_constants(entity)
        OrderingList.append(self, entity)

    def insert(self, index, entity):
        self._set_constants(entity)
        OrderingList.insert(self, index, entity)

    def remove(self, entity):
        self._unset_constants(entity)
        OrderingList.remove(self, entity)

    def pop(self, index=-1):
        entity = OrderingList.pop(self, index=index)
        self._unset_constants(entity)
        return entity

    def remove(self, entity):
        self._unset_constants(entity)
        OrderingList.remove(self, entity)
