# -*- coding: utf-8 -*-
# Copyright (C) 2018 - TODAY Luis Felipe Mileo - KMEE INFORMATICA LTDA
# License AGPL-3 - See https://www.gnu.org/licenses/lgpl-3.0.html

from __future__ import division, print_function, unicode_literals


from pynfe.utils.flags import (
    NAMESPACE_SOAP,
    NAMESPACE_XSI,
    NAMESPACE_XSD,
    MODELO_GNRE,
    NAMESPACE_GNRE,
    VERSAO_GNRE,
    GNRE_WS_METODO,
    NAMESPACE_GNRE_METODO,
    WS_GNRE_CONFIG,
    WS_GNRE_RECEPCAO,
    WS_GNRE_RET_RECEPCAO,
)
from pynfe.utils.webservices import GNRE
from pynfe.utils import etree, extrai_id_srtxml
from .comunicacao import Comunicacao
from .resposta import analisar_retorno

from gnrelib.gnrelib.v1_12 import consulta_config_uf


class ComunicacaoGNRE(Comunicacao):

    _modelo = MODELO_GNRE
    _namespace = NAMESPACE_GNRE
    _versao = VERSAO_GNRE
    _ws_metodo = GNRE_WS_METODO
    _header = 'gnreCabecMsg'
    _envio_mensagem = 'gnreDadosMsg'
    _namespace_metodo = NAMESPACE_GNRE_METODO
    _webservice = GNRE
    _accept = True
    _soap_action = False
    _namespace_soap = NAMESPACE_SOAP
    _namespace_xsi = NAMESPACE_XSI
    _namespace_xsd = NAMESPACE_XSD
    _soap_version = 'soap12'

    # _retorno_mensagem = 'mdfeRecepcaoResult'
    # _edoc_situacao_ja_enviado = MDFE_SITUACAO_JA_ENVIADO
    # _edoc_situacao_arquivo_recebido_com_sucesso = '103'
    # _edoc_situacao_em_processamento = '105'
    # _edoc_situacao_servico_em_operacao = '107'
    #
    # consulta_servico_ao_enviar = True
    # maximo_tentativas_consulta_recibo = 5

    def _get_url_webservice_metodo(self, ws_metodo):
        if self._ambiente == 1:
            ambiente = 'HTTPS'
        else:
            ambiente = 'HOMOLOGACAO'
        url = self._webservice['PE'][ambiente] + self._webservice['PE'][ws_metodo]
        webservice = self._ws_metodo[ws_metodo]['webservice']
        metodo = self._ws_metodo[ws_metodo]['metodo']
        return url, webservice, metodo

    def consultar_configuracao(self, uf, receita=None):
        raiz = consulta_config_uf.TConsultaConfigUf(
            ambiente=str(self._ambiente),
            uf=uf,
            # receita=receita,
        )
        return self._post_soap(
            classe=consulta_config_uf,
            ws_metodo=WS_GNRE_CONFIG,
            raiz_xml=raiz
        )
