# Dantotsu em Português (Brasil) — Build automático de hora em hora

> [!NOTE]
> - Este repositório **compila automaticamente** o branch **dev** do projeto oficial Dantotsu, aplicando uma **tradução para Português do Brasil (pt-BR)**:
> ➡️ [rebelonion/Dantotsu (branch dev)](https://git.rebelonion.dev/rebelonion/Dantotsu/src/branch/dev)
>
> - De hora em hora o workflow verifica se há novos commits no upstream.
> Se houver mudanças → um APK traduzido é compilado e publicado como release **neste próprio repositório**.
>
> - Todo o desenvolvimento do app é feito por [**rebelonion**](https://git.rebelonion.dev/rebelonion) e pelos [contribuidores oficiais](https://git.rebelonion.dev/rebelonion/Dantotsu/activity/contributors). Este repositório **não modifica o código-fonte** — apenas sobrepõe os textos traduzidos no momento do build.

## Como funciona

O código oficial fica em um Forgejo privado que exige chave SSH. Como este fork não tem essa chave, o build clona de um **espelho público no GitHub** do mesmo branch `dev` e aplica a tradução por cima.

1. **`check-updates`** — clona o espelho público, compara o último commit com o SHA do último release deste repositório e decide se precisa rebuildar.
2. **`build`** — clona o fonte, roda `scripts/apply_translation.py` para aplicar o pt-BR, compila o flavor **`fdroid`** (sem Firebase/Google Services), assina o APK e publica o release.

A tradução fica em [`translation/values-pt-rBR/strings.xml`](translation/values-pt-rBR/strings.xml). O script de overlay:

- Instala o idioma `pt-rBR` (dispositivos em Português do Brasil já veem tudo traduzido).
- **Sobrescreve os textos padrão** (`values/strings.xml`), então o app abre em Português **independente do idioma do aparelho**.
- Textos novos que o upstream adicionar e ainda não tiverem tradução continuam em inglês — o build nunca quebra por falta de tradução.

### Configuração (topo de [`.github/workflows/dantotsu-sync-release.yml`](.github/workflows/dantotsu-sync-release.yml))

| Variável | Padrão | Descrição |
| --- | --- | --- |
| `MIRROR_REPO` | `https://github.com/itsmechinmoy/Dantotsu.git` | Espelho público do fonte |
| `MIRROR_BRANCH` | `main` | Branch do espelho que segue o `dev` oficial |
| `BUILD_FLAVOR` | `fdroid` | Flavor compilado (sem Firebase) |

## Assinatura do APK

> [!IMPORTANT]
> Por padrão, o APK é assinado com a **chave debug** (funciona sem configurar nada).
>
> Para manter **a mesma assinatura entre builds** (necessário para atualizar pelo Obtainium sem desinstalar), adicione estes *secrets* no repositório (`Settings → Secrets and variables → Actions`):
>
> - `KEYSTORE_FILE` — keystore em base64 (`base64 -w0 sua.keystore`)
> - `KEYSTORE_PASSWORD`
> - `KEY_ALIAS`
> - `KEY_PASSWORD`
>
> Se esses secrets não existirem, o build cai automaticamente na assinatura debug.

## Atualizações

- Builds só são criados quando há novos commits no upstream — sem releases vazios.
- Você também pode rodar manualmente em **Actions → Build and Release Dantotsu (pt-BR) → Run workflow**.

## Problemas

- Bugs do **app em si**: reporte no tracker oficial → https://git.rebelonion.dev/rebelonion/Dantotsu/issues
- Erros de **tradução**: abra uma issue neste repositório.

## Créditos

Todo o crédito do aplicativo é de [**rebelonion**](https://git.rebelonion.dev/rebelonion) e dos [contribuidores oficiais](https://git.rebelonion.dev/rebelonion/Dantotsu/activity/contributors). Este repositório apenas adiciona a tradução pt-BR e automatiza os builds.
