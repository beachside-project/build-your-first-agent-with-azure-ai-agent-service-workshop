## Self-Guided Learners (自己学習者向け)

このページは、Self-Guided Learners **(自己学習者向け)** のコンテンツです。以下の手順に従って環境をセットアップし、ワークショップを開始してください。

## はじめに

このワークショップは、Azure AI Agents サービスと関連 SDK について学ぶことを目的としています。複数のラボで構成されており、各ラボでは Azure AI Agents サービスの特定の機能に焦点を当てています。各ラボは前のラボの知識と作業に基づいて構築されるため、順番に完了することを想定しています。

## 前提条件

1. Azure サブスクリプションへのアクセス。Azure サブスクリプションをお持ちでない場合は以下どちらかをお選びください。
  - COGBOT コミュニティより Azure AI Fundory を利用するためのキーなどを提供していただく。
  - [無料アカウント](https://azure.microsoft.com/free/){:target="_blank"}を作成する。
2. GitHub アカウントが必要です。お持ちでない場合は、[GitHub](https://github.com/join){:target="_blank"}で作成してください。

## ワークショップのプログラミング言語を選択

ワークショップは Python と C# の両方で利用可能です。該当箇所では、言語セレクタータブを使用して希望の言語を選択してください。注意：ラボの途中で言語を切り替えないでください。

**希望する言語のタブを選択してください：**

=== "Python"
    ワークショップのデフォルト言語は **Python** に設定されています。
=== "C#"
    ワークショップのデフォルト言語は **C#** に設定されています。

## ワークショップを開く

このワークショップを実行する推奨方法は、GitHub Codespaces を使用することです。このオプションは、ワークショップを完了するために必要なすべてのツールとリソースを備えた事前設定済みの環境を提供します。
または、Visual Studio Code の Dev Container を使用してローカルでワークショップを開くこともできます。


=== "GitHub Codespaces"

    **Open in GitHub Codespaces** をクリックして、GitHub Codespaces でプロジェクトを開きます。

    [![Open in GitHub Codespaces](https://github.com/codespaces/badge.svg)](https://codespaces.new/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop){:target="_blank"}

    !!! Warning "Codespace のビルドには数分かかります。ビルド中に指示を読み進めることができます。"

=== "VS Code Dev Container"
    
    ローカル環境でのトラブルが発生すると、ワークショップが全く進行できずタイムアップになる可能性があるため、ローカルで VS Code から Dev Container の利用に精通している方のみが利用してください。

    !!! warning "Apple Silicon ユーザー"
        まもなく実行する自動デプロイスクリプトは Apple Silicon ではサポートされていません。デプロイスクリプトは、Dev コンテナーではなく Codespaces または macOS から実行してください。

    Visual Studio Code Dev コンテナーを使用してローカルでプロジェクトを開くこともできます。これにより、[Dev Containers 拡張機能](https://marketplace.visualstudio.com/items?itemName=ms-vscode-remote.remote-containers){:target="_blank"}を使用して、ローカルの VS Code 開発環境でプロジェクトが開かれます。

    1. Docker Desktop を起動します（まだインストールされていない場合はインストールします）。
    2. **Dev Containers Open** を選択して、VS Code Dev コンテナーでプロジェクトを開きます。

        [![Dev Containers で開く](https://img.shields.io/static/v1?style=for-the-badge&label=Dev%20Containers&message=Open&color=blue&logo=visualstudiocode)](https://vscode.dev/redirect?url=vscode://ms-vscode-remote.remote-containers/cloneInVolume?url=https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop)

    !!! Warning "ローカルシステムでのダウンロードとセットアップを含む Dev コンテナーのビルドプロセスには数分かかります。この間、指示を読み進めることができます。"


## Azure の認証

!!! Warning "COGBOT コミュニティーより Azure サブスクリプションの情報を提供いただいている方は、「Azure の認証」「Azure のリソースをデプロイ」を飛ばして、「言語ワークスペースの選択」へ進みます"

Agent App が Azure AI Agents Service とモデルにアクセスできるように、Azure に認証する必要があります。以下の手順に従ってください：

1. Codespace が作成されていることを確認します。
2. Codespace で、**VS Code メニュー**から**ターミナル** > **新しいターミナル**を選択して、新しいターミナルウィンドウを開きます。
3. 次のコマンドを実行して Azure に認証します：

    ```shell
    az login --use-device-code
    ```

    !!! note
        ブラウザリンクを開き、Azure アカウントにログインするように求められます。最初に認証コードをコピーしてください。

        1. ブラウザウィンドウが自動的に開き、アカウントの種類を選択して**次へ**をクリックします。
        2. Azure サブスクリプションの**ユーザー名**と**パスワード**でサインインします。
        3. 認証コードを**貼り付け**ます。
        4. **OK**、次に**完了**を選択します。

    !!! warning
        複数の Azure テナントをお持ちの場合は、認証時に適切なテナントを選択する必要があります。

        ```shell
        az login --use-device-code --tenant <tenant_id>
        ```

1. 次に、コマンドラインから適切なサブスクリプションを選択します。
2. 次のステップのためにターミナルウィンドウを開いたままにしておきます。

## Azure のリソースをデプロイ

以下のリソースが、Azure サブスクリプションの `rg-contoso-agent-workshop` リソースグループに作成されます。

* **agent-wksp** という名前の **Azure AI Foundry Hub**
* **Agent Service Workshop** という名前の **Azure AI Foundry project**
* **gpt-4o (Global 2024-08-06)** という名前の **サーバーレス (従量課金制) GPT-4o モデルのデプロイメント**。価格の詳細はこちら[こちら](https://azure.microsoft.com/pricing/details/cognitive-services/openai-service/){:target="_blank"}。
* **Grounding with Bing Search** というリソース。[ドキュメント](https://learn.microsoft.com/azure/ai-services/agents/how-to/tools/bing-grounding)と[価格](https://www.microsoft.com/en-us/bing/apis/grounding-pricing){:target="_blank"}で詳細をご覧ください。

!!! warning "gpt-4o Global Standard SKU で 140K TPM のクォータ可用性が必要です。これは、エージェントが大量のトークンを使用するためではなく、エージェントがモデルに対して行う呼び出しの頻度のためです。[AI Foundry Management Center](https://ai.azure.com/managementCenter/quota){:target="_blank"}でクォータの可用性を確認してください。"

ワークショップに必要なリソースのデプロイを自動化するための bash スクリプトを提供しています。または、Azure AI Foundry スタジオを使用して手動でリソースをデプロイすることもできます。希望するタブを選択してください。


=== "自動デプロイ"

    スクリプト `deploy.sh` は、デフォルトで `eastus2` リージョンにデプロイします。リージョンまたはリソース名を変更するには、ファイルを編集してください。スクリプトを実行するには、VS Code ターミナルを開き、次のコマンドを実行します：

    ```bash
    cd infra && ./deploy.sh
    ```

    ### ワークショップ構成

    === "Python"

        デプロイスクリプトは、プロジェクト接続文字列、モデルデプロイメント名、および Bing 接続名を含む **.env** ファイルを生成します。

        **.env** ファイルは、プロジェクト接続文字列を除いて、次のように表示されるはずです。

        ```python
        MODEL_DEPLOYMENT_NAME="gpt-4o"
        BING_CONNECTION_NAME="groundingwithbingsearch"
        PROJECT_CONNECTION_STRING="<your_project_connection_string>"
        ```
    === "C#"

        自動デプロイスクリプトは、[ASP.NET Core での開発におけるアプリシークレットの安全な保存](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}のためのシークレットマネージャー機能を使用して、プロジェクト変数を安全に保存します。

        次のコマンドを実行してシークレットを表示できます：

        ```bash
        dotnet user-secrets list
        ```

=== "手動デプロイ"

    または、`deploy.sh` スクリプトを使用したくない場合は、次のように Azure AI Foundry ポータルを使用して手動でリソースをデプロイできます：

    1. ブラウザを使用して [Azure AI Foundry](https://ai.azure.com){:target="_blank"} Web ポータルに移動し、アカウントでサインインします。
    2. **+ プロジェクトを作成**を選択します。

        * プロジェクトに名前を付けます

            ```text
            agent-workshop
            ```

        * 次の名前で新しいハブを作成します

            ```text
            agent-workshop-hub
            ```

        * **作成**を選択し、プロジェクトが作成されるのを待ちます。
    3. **マイ アセット**から、**モデル + エンドポイント**を選択します。
    4. **モデルのデプロイ / 基本モデルのデプロイ**を選択します。

        * モデルリストから **gpt-4o** を選択し、**確認**を選択します。
        * デプロイメントに名前を付けます

            ```text
            gpt-4o
            ```

        * デプロイメントタイプ：**Global Standard** を選択します。
        * **カスタマイズ**を選択します。
        * モデルバージョン：**2024-08-06** を選択します。
        * 1分あたりのトークン数レート制限：**140k** を選択します。
        * **デプロイ**を選択します。

    !!! note
        プロジェクトをデプロイしたリージョンによっては、特定のバージョンの GPT-4o が必要になる場合があります。
        詳細は[モデル: アシスタント (プレビュー)](https://learn.microsoft.com/en-us/azure/ai-services/openai/concepts/models?tabs=global-standard%2Cstandard-chat-completions#assistants-preview){:target="_blank"}を参照してください。

    ### ワークショップ構成

    エージェントアプリを Azure AI Foundry プロジェクトに接続するには、プロジェクト接続文字列が必要です。この文字列は、Azure AI Foundry ポータルのプロジェクト `agent-workshop` の概要ページ（プロジェクト詳細セクション内）にあります。

    === "Python"

        次のコマンドを使用してワークショップ構成ファイルを作成します：

        ```bash
        cp src/workshop/.env.sample src/workshop/.env
        ```

        次に、ファイル `src/workshop/.env` を編集して、プロジェクト接続文字列を指定します。

    === "C#"

        1. VS Code で新しいターミナルウィンドウを開きます。
        2. 次のコマンドを実行して、C# プロジェクトパス $CSHARP_PROJECT_PATH 変数を設定します：

            ```bash
            CSHARP_PROJECT_PATH="src/csharp/workshop/AgentWorkshop.Client/AgentWorkshop.Client.csproj"
            ```
        3. 次のコマンドを実行して、プロジェクト接続文字列の [ASP.NET Core 安全なシークレット](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}を設定します：

            !!! warning "`<your_project_connection_string>` を実際の接続文字列に置き換えてください"

            ```bash
            dotnet user-secrets set "ProjectConnectionString" "<your_project_connection_string>" --project "$CSHARP_PROJECT_PATH"
            ```

        4. 次のコマンドを実行して、モデルデプロイメント名の [ASP.NET Core 安全なシークレット](https://learn.microsoft.com/aspnet/core/security/app-secrets){:target="_blank"}を設定します：

            ```bash
            dotnet user-secrets set "Azure:ModelName" "gpt-4o" --project "$CSHARP_PROJECT_PATH"
            ```

## 言語ワークスペースの選択

ワークショップには、Python 用と C# 用の 2 つのワークスペースがあります。ワークスペースには、各言語のラボを完了するために必要なソースコードとすべてのファイルが含まれています。使用したい言語に一致するワークスペースを選択してください。

=== "Python"

    1. **VS Code メニュー**から、**ファイル** > **ファイルでワークスペースを開く**を選択します。
    2. **.vscode/python-workspace.code-workspace** ファイルを選択します。

    ## プロジェクト構造

    ワークショップ全体を通して作業する主要な**サブフォルダ**と**ファイル**についてよく理解しておいてください。

    ### workshop フォルダ

    * **main.py** ファイル：アプリのエントリポイントで、主要なロジックが含まれています。
    * **sales_data.py** ファイル：SQLite データベースに対して動的 SQL クエリを実行する関数ロジック。
    * **stream_event_handler.py** ファイル：トークンストリーミングのイベントハンドラーロジックが含まれています。

    ### shared フォルダ

    * **files** フォルダ：エージェントアプリによって作成されたファイルが含まれています。
    * **fonts** フォルダ：コードインタープリターで使用される多言語フォントが含まれています。
    * **instructions** フォルダ：LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](../media/project-structure-self-guided-python.png)

=== "C#"

    1. **VS Code メニュー**から、**ファイル** > **ファイルでワークスペースを開く**を選択します。
    2. **.vscode/csharp-workspace.code-workspace** ファイルを選択します。

    ## プロジェクト構造

    ワークショップ全体を通して作業する主要な**サブフォルダ**と**ファイル**についてよく理解しておいてください。

    ### workshop フォルダ

    * **Lab1.cs, Lab2.cs, Lab3.cs** ファイル：各ラボのエントリポイントで、そのエージェントロジックが含まれています。
    * **Program.cs** ファイル：アプリのエントリポイントで、主要なロジックが含まれています。
    * **SalesData.cs** ファイル：SQLite データベースに対して動的 SQL クエリを実行する関数ロジック。

    ### shared フォルダ

    * **files** フォルダ：エージェントアプリによって作成されたファイルが含まれています。
    * **fonts** フォルダ：コードインタープリターで使用される多言語フォントが含まれています。
    * **instructions** フォルダ：LLM に渡される指示が含まれています。

    ![ラボフォルダ構造](../media/project-structure-self-guided-csharp.png)