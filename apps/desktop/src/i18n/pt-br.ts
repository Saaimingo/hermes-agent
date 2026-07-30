import { defineLocale } from './define-locale'

export const ptBr = defineLocale({
  common: {
    apply: 'Aplicar',
    back: 'Voltar',
    save: 'Salvar',
    saving: 'Salvando…',
    cancel: 'Cancelar',
    change: 'Alterar',
    choose: 'Escolher',
    clear: 'Limpar',
    close: 'Fechar',
    collapse: 'Recolher',
    confirm: 'Confirmar',
    connect: 'Conectar',
    connecting: 'Conectando…',
    continue: 'Continuar',
    copied: 'Copiado',
    copy: 'Copiar',
    copyFailed: 'Falha ao copiar',
    delete: 'Excluir',
    docs: 'Documentação',
    done: 'Concluído',
    error: 'Erro',
    expand: 'Expandir',
    failed: 'Falhou',
    formatJson: 'Formatar JSON',
    free: 'Grátis',
    loading: 'Carregando…',
    notSet: 'Não definido',
    refresh: 'Atualizar',
    remove: 'Remover',
    replace: 'Substituir',
    retry: 'Tentar novamente',
    run: 'Executar',
    send: 'Enviar',
    set: 'Definir',
    skip: 'Pular',
    update: 'Atualizar',
    tryHint: (term: string) => `Tente "${term}"`,
    on: 'Ligado',
    off: 'Desligado'
  },

  fileMenu: {
    revealFinder: 'Mostrar no Finder',
    revealExplorer: 'Mostrar no Explorer',
    revealFileManager: 'Mostrar no gerenciador de arquivos',
    revealInSidebar: 'Revelar na barra lateral',
    copyPath: 'Copiar caminho',
    copyRelativePath: 'Copiar caminho relativo',
    rename: 'Renomear…',
    delete: 'Excluir',
    renameTitle: 'Renomear',
    renameLabel: 'Novo nome',
    deleteTitle: (name: string) => `Excluir ${name}?`,
    deleteBody: 'Move para a lixeira. Pode ser restaurado de lá.',
    pathCopied: 'Caminho copiado'
  },

  boot: {
    ready: 'Hermes Desktop pronto',
    desktopBootFailedWithMessage: (message: string) => `Falha ao iniciar o Desktop: ${message}`,
    steps: {
      connectingGateway: 'Conectando ao gateway do desktop…',
      loadingSettings: 'Carregando configurações do Hermes…',
      loadingSessions: 'Carregando sessões recentes…',
      startingDesktopConnection: 'Iniciando conexão do desktop…',
      startingHermesDesktop: 'Iniciando Hermes Desktop…'
    },
    errors: {
      backgroundExited: 'O processo em segundo plano do Hermes foi encerrado.',
      backgroundExitedDuringStartup: 'O processo em segundo plano do Hermes foi encerrado durante a inicialização.',
      backendStopped: 'O backend parou',
      desktopBootFailed: 'Falha ao iniciar o desktop',
      gatewayConnectionLost: 'Conexão com o gateway perdida',
      gatewaySignInRequired: 'É necessário fazer login no gateway',
      ipcBridgeUnavailable: 'A ponte IPC do desktop não está disponível.'
    },
    failure: {
      title: 'Não foi possível iniciar o Hermes',
      description:
        'O gateway em segundo plano não iniciou. Tente as etapas de recuperação abaixo. Seus chats e configurações não serão apagados.',
      remoteTitle: 'É necessário fazer login no gateway remoto',
      remoteDescription:
        'Sua sessão do gateway remoto expirou. Faça login novamente para reconectar. Seus chats e configurações não serão apagados.',
      retry: 'Tentar novamente',
      repairInstall: 'Reparar instalação',
      useLocalGateway: 'Usar gateway local',
      gatewaySettings: 'Configurações do gateway',
      back: 'Voltar',
      openLogs: 'Abrir logs',
      repairHint: 'O reparo reinstala o instalador. Em máquinas novas pode levar alguns minutos.',
      remoteSignInHint: (signInLabel: string) =>
        `Sai da sessão remota salva no navegador e abre ${signInLabel}. Use "Usar gateway local" para alternar para o backend incluído.`,
      signOutAndSignIn: 'Sair e entrar novamente',
      remoteFailureHint:
        'Verifique a URL do gateway e o login nas configurações do Gateway, ou alterne para o gateway local.',
      hideRecentLogs: 'Ocultar logs recentes',
      showRecentLogs: 'Mostrar logs recentes',
      signedInTitle: 'Conectado',
      signedInMessage: 'Reconectando ao gateway remoto…',
      signInIncompleteTitle: 'Login incompleto',
      signInIncompleteMessage: 'A janela de login fechou antes da autenticação terminar.',
      signInFailed: 'Falha no login',
      signInToRemoteGateway: 'Entrar no gateway remoto',
      signInWithProvider: (provider: string) => `Entrar com ${provider}`,
      identityProvider: 'Provedor de identidade'
    }
  },

  language: {
    label: 'Idioma',
    description: 'Escolha o idioma da interface do Hermes Desktop.',
    saving: 'Salvando idioma…',
    saveError: 'Erro ao atualizar o idioma',
    switchTo: 'Trocar idioma',
    searchPlaceholder: 'Buscar idiomas…',
    noResults: 'Nenhum idioma encontrado'
  },

  notifications: {
    region: 'Notificações',
    hide: 'Ocultar',
    show: 'Mostrar',
    more: (count: number) => `+${count} mais`,
    clearAll: 'Limpar tudo',
    dismiss: 'Dispensar notificação',
    details: 'Detalhes',
    copyDetail: 'Copiar detalhe',
    copyDetailFailed: 'Falha ao copiar detalhe da notificação',
    backendOutOfDateTitle: 'Backend desatualizado',
    backendOutOfDateMessage:
      'Seu backend do Hermes está mais antigo que esta versão do desktop e pode não funcionar corretamente. Atualize para alinhá-los.',
    installMethodUnsupportedTitle: 'Método de instalação não suportado',
    updateHermes: 'Atualizar Hermes',
    updateReadyTitle: 'Atualização pronta',
    updateReadyMessage: (count: number) => `${count} nova(s) alteração(ões) disponível(is).`,
    seeWhatsNew: 'Ver novidades',
    errors: {
      elevenLabsNeedsKey: 'ElevenLabs STT precisa de ELEVENLABS_API_KEY.',
      elevenLabsRejectedKey: 'A ElevenLabs rejeitou a chave de API (401).',
      gatewayAuthFailed: 'Falha na autenticação do gateway — verifique sua API_SERVER_KEY.',
      methodNotAllowed:
        'O backend do desktop rejeitou a requisição (405 Method Not Allowed). Tente reiniciar o Hermes Desktop.',
      microphonePermission: 'Permissão de microfone negada.',
      openaiRejectedApiKey: 'A OpenAI rejeitou a OPENAI_API_KEY.',
      openaiRejectedApiKeyWithStatus: (status: string) =>
        `A OpenAI rejeitou a chave de API (${status} invalid_api_key).`,
      openaiTtsNeedsKey: 'O TTS da OpenAI precisa de VOICE_TOOLS_OPENAI_KEY ou OPENAI_API_KEY.'
    },
    voice: {
      configureSpeechToText: 'Configure fala-para-texto para usar o modo de voz.',
      couldNotStartSession: 'Não foi possível iniciar a sessão de voz',
      microphoneAccessDenied: 'Acesso ao microfone negado.',
      microphoneConstraintsUnsupported: 'Restrições de microfone não são suportadas por este dispositivo.',
      microphoneFailed: 'Falha no microfone',
      microphoneInUse: 'O microfone já está em uso por outro aplicativo.',
      microphonePermissionDenied: 'Permissão de microfone negada.',
      microphoneStartFailed: 'Não foi possível iniciar a gravação do microfone.',
      microphoneUnsupported: 'Este ambiente não suporta gravação de microfone.',
      noMicrophone: 'Nenhum microfone encontrado.',
      noSpeechDetected: 'Nenhuma fala detectada',
      playbackFailed: 'Falha na reprodução de voz',
      recordingFailed: 'Falha na gravação de voz',
      transcriptionFailed: 'Falha na transcrição de voz',
      transcriptionUnavailable: 'A transcrição de voz ainda não está disponível.',
      tryRecordingAgain: 'Tente gravar novamente.',
      unavailable: 'Voz indisponível'
    },
    native: {
      approvalTitle: 'Aprovação necessária',
      approveAction: 'Aprovar',
      rejectAction: 'Rejeitar',
      inputTitle: 'Entrada necessária',
      inputBody: 'O Hermes está aguardando sua resposta.',
      turnDoneTitle: 'Hermes concluiu',
      turnDoneBody: 'A resposta está pronta.',
      turnErrorTitle: 'Turno falhou',
      backgroundDoneTitle: 'Tarefa em segundo plano concluída',
      backgroundFailedTitle: 'Tarefa em segundo plano falhou',
      creditsTitle: 'Créditos'
    }
  },

  remoteDisplayBanner: {
    message: (reason: string) =>
      `Renderização por software ativa — exibição remota detectada (${reason}). Aceleração de GPU desativada para evitar cintilação.`
  },

  titlebar: {
    hideSidebar: 'Ocultar barra lateral',
    showSidebar: 'Mostrar barra lateral',
    search: 'Buscar',
    searchTitle: 'Buscar sessões, visualizações e ações',
    swapSidebarSides: 'Inverter barras laterais',
    swapSidebarSidesTitle: 'Trocar a posição das barras de sessões e arquivos',
    hideRightSidebar: 'Ocultar barra lateral direita',
    showRightSidebar: 'Mostrar barra lateral direita',
    muteHaptics: 'Silenciar feedback tátil',
    unmuteHaptics: 'Ativar feedback tátil',
    openSettings: 'Abrir configurações',
    openStarmap: 'Abrir grafo de memória',
    openKeybinds: 'Atalhos de teclado',
    layoutEditor: 'Editor de layout',
    layoutEditorTitle: 'Editor de layout — ⌘-clique redefine o layout'
  },

  keybinds: {
    title: 'Atalhos de teclado',
    subtitle: (open: string) => `Clique em um atalho para reatribuí-lo · ${open} reabre este painel.`,
    search: 'Buscar atalhos…',
    rebind: 'Reatribuir',
    reset: 'Restaurar padrão',
    resetAll: 'Restaurar todos',
    pressKey: 'Pressione uma tecla…',
    set: 'definir',
    conflictWith: (label: string) => `Também vinculado a "${label}"`,
    categories: {} as Record<string, string>,
    actions: {} as Record<string, string>
  },

  findInPage: {
    next: 'Próxima ocorrência',
    previous: 'Ocorrência anterior'
  },

  settings: {
    closeSettings: 'Fechar configurações',
    exportConfig: 'Exportar configuração',
    importConfig: 'Importar configuração',
    resetToDefaults: 'Restaurar padrões',
    resetConfirm: 'Redefinir todas as configurações para os padrões do Hermes?',
    exportFailed: 'Falha ao exportar',
    resetFailed: 'Falha ao redefinir',
    nav: {
      providers: 'Provedores',
      providerAccounts: 'Contas',
      providerApiKeys: 'Chaves de API',
      providerCustomEndpoints: 'Endpoints personalizados',
      gateway: 'Gateway',
      apiKeys: 'Ferramentas e Chaves',
      keybinds: 'Atalhos de Teclado',
      keysTools: 'Ferramentas',
      keysSettings: 'Configurações',
      mcp: 'MCP',
      archivedChats: 'Chats Arquivados',
      about: 'Sobre',
      billing: 'Faturamento',
      notifications: 'Notificações',
      plugins: 'Plugins'
    },
    plugins: {
      title: 'Plugins do desktop',
      blurb:
        'Extensões de interface carregadas neste app — incluídas na versão ou adicionadas na pasta desktop-plugins (incluindo as que o Hermes grava). Desativar descarrega o plugin em tempo real e sobrevive a reinicializações.',
      count: (n: number) => `${n} instalado(s)`,
      openFolder: 'Abrir pasta de plugins',
      rescan: 'Reescanear',
      reveal: 'Revelar no gerenciador de arquivos',
      enable: 'Ativar',
      disable: 'Desativar',
      failed: 'falhou',
      empty: 'Nenhum plugin de desktop instalado.',
      kinds: { bundled: 'incluído', disk: 'em disco', runtime: 'runtime' }
    },
    notifications: {
      title: 'Notificações',
      intro:
        'Notificações nativas do desktop, separadas dos toasts do app. São locais ao dispositivo — cada computador mantém suas próprias configurações.',
      enableAll: 'Ativar notificações',
      enableAllDesc: 'Interruptor principal. Desative para silenciar todas as notificações abaixo.',
      focusedHint: 'Alertas de conclusão só disparam quando o Hermes está em segundo plano.',
      kinds: {
        approval: {
          label: 'Aprovação necessária',
          description: 'Um comando está aguardando você aprová-lo ou rejeitá-lo.'
        },
        input: {
          label: 'Entrada necessária',
          description: 'O Hermes fez uma pergunta ou precisa de senha ou segredo.'
        },
        turnDone: {
          label: 'Resposta pronta',
          description: 'Um turno terminou enquanto o Hermes estava em segundo plano.'
        },
        turnError: {
          label: 'Turno falhou',
          description: 'Um turno terminou com erro.'
        },
        backgroundDone: {
          label: 'Tarefa em segundo plano concluída',
          description: 'Um comando de terminal em segundo plano foi concluído.'
        },
        credits: {
          label: 'Alertas de crédito',
          description: 'Acesso a créditos foi pausado ou restaurado.'
        }
      },
      test: 'Enviar notificação de teste',
      testTitle: 'Hermes',
      testBody: 'As notificações estão funcionando.',
      testSent:
        'Teste enviado. Se nada aparecer, verifique as permissões de notificação do sistema e o modo Foco/Não Perturbe.',
      testUnsupported: 'Este sistema não suporta notificações nativas.',
      completionSoundTitle: 'Som de conclusão',
      completionSoundDesc:
        'Toca quando um turno do agente termina. Escolha um som e pré-visualize aqui.',
      completionSoundPreview: 'Pré-visualizar'
    },
    sections: {} as Record<string, string>,
    modeOptions: {
      light: { label: 'Claro', description: 'Superfícies claras no desktop' },
      dark: { label: 'Escuro', description: 'Ambiente de baixo brilho' },
      system: { label: 'Sistema', description: 'Seguir aparência do sistema' }
    },
    appearance: {
      title: 'Aparência',
      intro:
        'Estas são preferências de exibição apenas do desktop. O modo controla o brilho; o tema controla a paleta de destaque e o estilo da superfície do chat.',
      colorMode: 'Modo de cor',
      colorModeDesc: 'Escolha um modo fixo ou permita que o Hermes siga a configuração do sistema.',
      toolViewTitle: 'Exibição de chamadas de ferramenta',
      toolViewDesc:
        'Produto oculta dados brutos das ferramentas; Técnico mostra entrada/saída completas.',
      uiScaleTitle: 'Escala da interface',
      uiScaleDesc: (percent: number) =>
        `Ajusta texto e controles em todo o app. Cmd/Ctrl com +, - e 0 também funciona. Atual: ${percent}%.`,
      translucencyTitle: 'Translucidez da janela',
      translucencyDesc:
        'Veja seu desktop através da janela inteira. Apenas macOS e Windows.',
      backdropTitle: 'Fundo do chat',
      backdropDesc: 'A imagem de estátua sutil atrás da conversa.',
      embedsTitle: 'Incorporações inline',
      embedsDesc:
        'Pré-visualizações ricas carregam de sites de terceiros (YouTube, X, …). Perguntar mostra um placeholder até você permitir cada um; Sempre carrega automaticamente; Desligado mantém links simples.',
      embedsAsk: 'Perguntar',
      embedsAlways: 'Sempre',
      embedsOff: 'Desligado',
      embedsReset: (count: number) =>
        `Redefinir ${count} ${count === 1 ? 'serviço permitido' : 'serviços permitidos'}`,
      product: 'Produto',
      productDesc: 'Atividade de ferramentas amigável com resumos concisos.',
      technical: 'Técnico',
      technicalDesc: 'Incluir argumentos/resultados brutos das ferramentas e detalhes de baixo nível.',
      themeTitle: 'Tema',
      themeDesc:
        'Apenas paletas do desktop. O modo selecionado é aplicado por cima.',
      themeProfileNote: (profile: string) =>
        `Salvo para o perfil ${profile} — cada perfil mantém seu próprio tema.`,
      installTitle: 'Instalar do VS Code',
      installDesc:
        'Cole um id de extensão do Marketplace (ex.: dracula-theme.theme-dracula) para converter seu tema de cores em uma paleta do desktop.',
      installPlaceholder: 'publisher.extension',
      installButton: 'Instalar',
      installing: 'Instalando…',
      installError: 'Não foi possível instalar esse tema.',
      installed: (name: string) => `"${name}" instalado.`,
      removeTheme: 'Remover tema',
      importedBadge: 'Importado',
      pet: {
        title: 'Pet',
        intro:
          'Adote um mascote animado da petdex que flutua sobre o app e reage ao que o Hermes está fazendo — correndo enquanto ferramentas executam, celebrando ao concluir, emburrando com erros.',
        restartHint:
          'Pets precisam de uma reinicialização rápida — o app em execução iniciou antes deste recurso ser adicionado. Saia e reabra o Hermes, depois volte aqui.',
        on: 'Ligado',
        off: 'Desligado',
        scaleTitle: 'Tamanho',
        scaleDesc: 'Redimensione o mascote flutuante. Aplica-se em todos os lugares instantaneamente.',
        roamTitle: 'Vagar',
        roamDesc: 'Permitir que o pet vagueie pela janela sozinho quando ocioso.',
        chooseTitle: 'Escolher um pet',
        chooseDesc: 'Selecionar um o instala (se necessário) e o torna ativo.',
        searchPlaceholder: 'Buscar pets…',
        unreachable:
          'Não foi possível acessar a galeria petdex. Verifique sua conexão e reabra esta página.',
        noMatch: (query: string) => `Nenhum pet corresponde a "${query}".`,
        installedTag: 'instalado',
        generatedTag: 'Gerado',
        countCapped: (cap: number, total: number) =>
          `Mostrando ${cap} de ${total} — digite para filtrar.`,
        count: (n: number) => `${n} pet${n === 1 ? '' : 's'}.`,
        uninstall: (name: string) => `Desinstalar ${name}`,
        delete: (name: string) => `Excluir ${name}`,
        deleteTitle: (name: string) => `Excluir ${name}?`,
        deleteBody: 'Isto exclui permanentemente o pet — não pode ser reinstalado.',
        deleteConfirm: 'Excluir',
        rename: (name: string) => `Renomear ${name}`,
        renameTitle: 'Renomear pet',
        renamePlaceholder: 'Nomeie seu pet',
        renameSave: 'Salvar',
        exportPet: (name: string) => `Exportar ${name}`,
        adoptFailed: (slug: string) => `Não foi possível adotar ${slug}`,
        uninstallFailed: (slug: string) => `Não foi possível desinstalar ${slug}`,
        renameFailed: (slug: string) => `Não foi possível renomear ${slug}`,
        exportFailed: (slug: string) => `Não foi possível exportar ${slug}`,
        noneAvailable: 'Nenhum pet disponível para ativar no momento.',
        turnOnFailed: 'Não foi possível ligar o pet.',
        turnOffFailed: 'Não foi possível desligar o pet.'
      }
    },
    fieldLabels: {} as Record<string, string>,
    fieldDescriptions: {} as Record<string, string>,
    about: {
      heading: 'Hermes Desktop',
      version: (value: string) => `Versão ${value}`,
      versionUnavailable: 'Versão indisponível',
      updates: 'Atualizações',
      checkNow: 'Verificar agora',
      checking: 'Verificando…',
      seeWhatsNew: 'Ver novidades',
      updateNow: 'Atualizar agora',
      releaseNotes: 'Notas de versão',
      onLatest: 'Você está na versão mais recente.',
      installing: 'Uma atualização está sendo instalada.',
      cantUpdate: 'Esta versão não pode se atualizar de dentro do app.',
      cantReach: 'Não foi possível alcançar o servidor de atualizações.',
      tapCheck: 'Toque em "Verificar agora" para buscar atualizações.',
      updateReady: (count: number) =>
        `Uma nova atualização está pronta (${count} ${count === 1 ? 'alteração incluída' : 'alterações incluídas'}).`,
      lastChecked: (age: string) => `Última verificação ${age}`,
      justNowSuffix: ' · agora mesmo',
      automaticUpdates: 'Atualizações automáticas',
      automaticUpdatesDesc:
        'O Hermes verifica atualizações automaticamente em segundo plano e avisa quando há uma disponível.',
      branchCommit: (branch: string, commit: string) => `Branch ${branch} · Commit ${commit}`,
      never: 'nunca',
      justNow: 'agora mesmo',
      minAgo: (count: number) => `${count} min atrás`,
      hoursAgo: (count: number) => `${count} horas atrás`,
      daysAgo: (count: number) => `${count} dias atrás`
    },
    config: {
      none: 'Nenhum',
      noneParen: '(nenhum)',
      builtinOnly: 'Apenas embutidos',
      notSet: 'Não definido',
      commaSeparated: 'valores separados por vírgula',
      loading: 'Carregando configuração do Hermes…',
      emptyTitle: 'Nada para configurar',
      emptyDesc: 'Esta seção não tem configurações ajustáveis.',
      failedLoad: 'Falha ao carregar configurações',
      autosaveFailed: 'Falha no salvamento automático',
      imported: 'Configuração importada',
      invalidJson: 'JSON de configuração inválido',
      keepAwakeTitle: 'Manter computador acordado',
      keepAwakeDesc:
        'Impedir que esta máquina durma para que execuções longas continuem. A tela ainda pode escurecer.'
    },
    quickEntry: {
      enabledTitle: 'Entrada rápida',
      enabledDesc:
        'Invoque um compositor compacto de qualquer lugar com um atalho global e envie um prompt sem abrir o Hermes.',
      shortcutTitle: 'Atalho da entrada rápida',
      shortcutDesc:
        'Precisa de pelo menos uma tecla modificadora, ex.: CommandOrControl+Shift+Space.',
      active: 'O atalho está ativo.',
      takenBy: 'Outro app já usa este atalho — escolha um diferente.',
      invalidShortcut: 'Atalho inválido. Inclua pelo menos uma tecla modificadora.'
    },
    credentials: {
      pasteKey: 'Colar chave',
      pasteLabelKey: (label: string) => `Colar chave ${label}`,
      optional: 'Opcional',
      enterValueFirst: 'Digite um valor primeiro.',
      couldNotSave: 'Não foi possível salvar a credencial.',
      remove: 'Remover',
      getKey: 'Obter uma chave',
      saving: 'Salvando'
    },
    envActions: {
      actionsFor: (label: string) => `Ações para ${label}`,
      credentialActions: 'Ações de credencial',
      manageInKeys: 'Gerenciar em Chaves de API',
      docs: 'Documentação',
      hideValue: 'Ocultar valor',
      revealValue: 'Revelar valor',
      replace: 'Substituir',
      set: 'Definir',
      clear: 'Limpar'
    },
    gateway: {
      loading: 'Carregando configurações do gateway…',
      unavailableTitle: 'Configurações do gateway indisponíveis',
      unavailableDesc:
        'A ponte IPC do desktop não expõe as configurações do gateway.',
      title: 'Conexão do Gateway',
      envOverride: 'sobrescrita de ambiente',
      intro:
        'O Hermes Desktop inicia seu próprio gateway local por padrão. Use um gateway remoto quando quiser que este app controle um backend do Hermes já em execução em outra máquina ou atrás de um proxy confiável. Escolha um perfil abaixo para dar a ele seu próprio host remoto.',
      appliesTo: 'Aplica-se a',
      allProfiles: 'Todos os perfis',
      defaultConnection:
        'Conexão padrão para todos os perfis que não possuem substituição própria.',
      profileConnection: (profile: string) =>
        `Conexão usada apenas quando "${profile}" é o perfil ativo. Escolha "Usar gateway padrão" para remover a substituição.`,
      envOverrideTitle:
        'Variáveis de ambiente estão controlando esta sessão do desktop.'
    }
  }
})
