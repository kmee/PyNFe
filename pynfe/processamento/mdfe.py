# -*- coding: utf-8 -*-
import re
import ssl
import datetime
import requests
from pynfe.utils import etree, so_numeros
from pynfe.utils.flags import (
    NAMESPACE_NFE,
    NAMESPACE_XSD,
    NAMESPACE_XSI,
    VERSAO_PADRAO,
    NAMESPACE_SOAP,
    CODIGOS_ESTADOS,
    NAMESPACE_BETHA,
    NAMESPACE_METODO,
)

from mdfelib.v3_00.consStatServMDFe import TConsStatServ

from .comunicacao import ComunicacaoSefaz

try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

from pynfe.utils.flags import (
    NAMESPACE_MDFE,
    MODELO_MDFE,
    NAMESPACE_MDFE_METODO,
)
from pynfe.utils.webservices import (
    MDFE_WS_URL,
    MDFE_WS_METODO,
    WS_MDFE_RECEPCAO,
    WS_MDFE_RET_RECEPCAO,
    WS_MDFE_RECEPCAO_EVENTO,
    WS_MDFE_CONSULTA,
    WS_MDFE_STATUS_SERVICO,
    WS_MDFE_CONSULTA_NAO_ENCERRADOS,
)

class ComunicacaoMDFE(ComunicacaoSefaz):

    _modelo = MODELO_MDFE
    _namespace = NAMESPACE_MDFE
    _versao = '3.00'
    _ws_url = MDFE_WS_URL
    _ws_metodo = MDFE_WS_METODO
    _header = 'mdfeCabecMsg'
    _envio_mensagem = 'mdfeDadosMsg'
    _retorno_mensagem = 'mdfeRecepcaoResult'
    _namespace_metodo = NAMESPACE_MDFE_METODO

    def _cabecalho_soap(self, metodo):
        """Monta o XML do cabeçalho da requisição SOAP"""

        raiz = etree.Element(
            self._header,
            xmlns=self._namespace_metodo + metodo
        )
        etree.SubElement(raiz, 'versaoDados').text = '3.00'
            # MDFE_WS_METODO[metodo]['versao']

        etree.SubElement(raiz, 'cUF').text = CODIGOS_ESTADOS[self.uf.upper()]
        return raiz

    def _get_url_metodo(self, ws_metodo):
        url = (
           'https://' +
           self._ws_url[self._ambiente]['servidor'] +
           '/' +
           self._ws_url[self._ambiente][ws_metodo]
        )
        metodo = self._ws_metodo[ws_metodo]['metodo']
        return url, metodo

    def status_servico(self):

        url, metodo = self._get_url_metodo(WS_MDFE_STATUS_SERVICO)

        raiz = TConsStatServ(
            versao=self._versao,
            tpAmb=str(self._ambiente),
            xServ='STATUS',
        )
        raiz.original_tagname_ = 'consStatServMDFe'

        xml = self._construir_xml_soap(
            metodo, self._construir_etree_ds(raiz)
        )

        return self._post(url, xml)

