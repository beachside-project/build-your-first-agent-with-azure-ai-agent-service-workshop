## はじめに

Bing でウェブ検索の結果を会話に含めることは、Azure AI Agent Service によって提供されるいくつかのツールの 1 つです。Grounding with Bing を使用すると、アプリは会話に関連する情報をウェブ検索できます。例えば、競合製品の情報を検索したい場合などです。

###Grounding with Bing へのアクセス

このラボでは Grounding with Bing のサービスが必要ですが、お使いの Azure サブスクリプションでは利用できない場合があります。アクセス権があるかどうかを確認するには、ラボの指示に従ってリソースを作成します。アクセス権がない場合は、エラーメッセージが表示されます。サービスを利用できない場合でも、Grounding with Bing がどのように機能するかを理解するために、必ずラボを読んでください。

## ラボ演習

このラボでは、Contoso の製品とカテゴリの競合売上分析を提供するために Grounding with Bing を有効にします。

## Grounding with Bing Search リソースの作成

Azure ポータルで **Grounding with Bing Search** リソースを作成し、それを Azure AI Foundry ポータルに接続する必要があります。

**Grounding with Bing Search** リソースを作成するには、次の手順に従います：

1.  [クリックして Grounding with Bing Search リソースを作成します](https://portal.azure.com/#view/Microsoft_Azure_Marketplace/GalleryItemDetailsBladeNopdl/id/Microsoft.BingGroundingSearch){:target="_blank"}。

    !!! Warning
        Azure ポータルにアクセスするには、Azure アカウントにサインインするか、ようこそ画面をクリアする必要がある場合があります。

2.  **作成**を選択します。
3.  ドロップダウンリストから **rg-agent-workshop** リソースグループを選択します。
4.  次のようにリソースに名前を付けます：

    ```text
    groundingwithbingsearch
    ```

5.  **Grounding with Bing Search** 価格レベルを選択します。
6.  **上記の通知を読み、理解したことを確認します (I confirm I have read and understood the notice above)** を確認します。
7.  **確認と作成**を選択します。
8.  **作成**を選択します。
9.  デプロイが完了するのを待ってから、**リソースに移動**をクリックします。
10. サイドバーメニューから**概要 (Overview)** を選択します。
11. **Azure AI Foundry ポータルに移動 (Go to Azure AI Foundry Portal)** ボタンを選択します。
<!-- 1. Select **Sign in** and enter your Azure account credentials. -->

## AI Foundry で Bing Search の接続を作成する

次に、Azure AI Foundry ポータルで Bing Search の接続を作成します。この接続により、Agent app は Agent の **Grounding with Bing Search** を使用して Bing Search サービスにアクセスできるようになります。

Azure AI Foundry ポータルで Bing Search 接続を作成するには、次の手順に従います：

1.  プロジェクト **Agent-Service-Workshop** が選択されていることを確認します。
2.  サイドバーメニューから **Management Center** ボタンをクリックします。ボタンはサイドバーの**下部**にピン留めされています。
3.  サイドバーメニューから **Connected resources** を選択します。
4.  **+ New connection** をクリックします。
5.  Knowledge セクションまでスクロールし、**Grounding with Bing Search** を選択します。
6.  `groundingwithbingsearch` リソースの右側にある **Add connection** ボタンをクリックします。
7.  **Close** をクリックします。

詳細については、[Grounding with Bing Search](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/bing-grounding){:target="_blank"} のドキュメントをご覧ください。

### Agent app で Grounding with Bing Search を有効にする

1.  `main.py` ファイルを開きます。

2.  **"# "** 文字を削除して、次の行の**コメントを解除**します

    ```python
    # INSTRUCTIONS_FILE = "instructions/bing_grounding.txt"

    # bing_connection = await project_client.connections.get(connection_name=BING_CONNECTION_NAME)
    # bing_grounding = BingGroundingTool(connection_id=bing_connection.id)
    # toolset.add(bing_grounding)
    ```

    !!! warning
        コメント解除する行は隣接していません。# 文字を削除する際は、その後のスペースも削除するようにしてください。

3.  `main.py` ファイルのコードを確認します。

    コメント解除後、コードは次のようになります：

    ```python
    INSTRUCTIONS_FILE = "instructions/function_calling.txt"
    INSTRUCTIONS_FILE = "instructions/file_search.txt"
    INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
    INSTRUCTIONS_FILE = "instructions/bing_grounding.txt"
    # INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"
    


    async def add_agent_tools() -> None:
        """Add tools for the agent."""
        font_file_info = None

        # 関数ツールを追加
        toolset.add(functions)

        # コードインタープリターツールを追加
        code_interpreter = CodeInterpreterTool()
        toolset.add(code_interpreter)

        # テントのデータシートを新しいベクトルデータストアに追加
        vector_store = await utilities.create_vector_store(
            project_client,
            files=[TENTS_DATA_SHEET_FILE],
            vector_store_name="Contoso Product Information Vector Store",
        )
        file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
        toolset.add(file_search_tool)

        # コードインタープリターに多言語サポートを追加
        # font_file_info = await utilities.upload_file(project_client, utilities.shared_files_path / FONTS_ZIP)
        # code_interpreter.add_file(file_id=font_file_info.id)

        # Bing グラウンディングツールを追加
        bing_connection = await project_client.connections.get(connection_name=BING_CONNECTION_NAME)
        bing_grounding = BingGroundingTool(connection_id=bing_connection.id)
        toolset.add(bing_grounding)

        return font_file_info
    ```

### 指示の確認

1.  **shared/instructions/bing_grounding.txt** ファイルを開きます。このファイルは、前のラボで使用された指示を置き換えます。

2.  **ツール**セクションには、「製品とカテゴリに関する競合インサイト (Competitive Insights for Products and Categories)」機能が含まれるようになり、Agentは次のことができるようになります：

      * Bing Search を使用して、競合他社の製品名、会社名、価格を収集します。
      * 応答を、アウトドアキャンプおよびスポーツ用品に関連するトピックに限定します。
      * 検索結果が簡潔で、クエリに直接関連していることを確認します。

### Agent app の実行

まず、以前と同様にターミナルからアプリを起動します：

1.  \<kbd\>F5\</kbd\> を押してアプリを実行します。

### Agent との会話を開始する

Agent は Contoso 売上データベース、テントデータシート、および Bing Search からのデータを組み合わせて包括的な応答を提供するため、結果はクエリによって異なります。

1.  **どの初心者向けテントを販売していますか？** (または「What beginner tents do we sell?」など)

    !!! info
        この情報は主に、ベクトル情報ストアで提供したファイルから取得されます。

2.  **競合他社はどの初心者向けテントを販売していますか？価格も含めて。** (または「What beginner tents do our competitors sell? Include prices.」など)

    !!! info
        この情報はインターネットから取得され、実世界の製品名と価格が含まれています。

3.  **棒グラフで表示して** (または「Show as a bar chart」など)

    !!! info
        AI Agent Service は再びコードインタープリターを使用してグラフを作成しますが、今回は前のクエリで取得した実世界のデータを使用します。以前と同様に、グラフを表示するには `shared/files` を確認してください。

4.  **競合他社の初心者向けテントと同様の価格帯で、私たちが地域別に販売しているテントを表示して** (または「Show the tents we sell by region that are a similar price to our competitors beginner tents.」など)

    !!! info
        このクエリは、基盤となる大規模言語モデルの推論能力と、関数呼び出しによって返されたデータに依存しています。

5.  **データを人間が読める JSON ファイルとしてダウンロードして** (または「Download the data as a human-readable JSON file」など)

    !!! info
        このクエリは再び、前のクエリのコンテキストからファイルを作成するためにコードインタープリターに依存しています。

### Agentアプリの停止

1.  **save** と入力して Agent アプリの状態を保存します。これにより、状態を削除せずに Agent app が停止し、Azure AI Foundry の Agents プレイグラウンドで Agent を探索できるようになります。

2.  \<kbd\>Shift\</kbd\>+\<kbd\>F5\</kbd\> を押して Agent app の**デバッグを停止**します。

3.  ターミナル出力から Agent ID を**コピー**します。Agent ID は、Azure AI Foundry ポータルで Agent を探索するために必要です。Agent ID は次のような形式になります：

    ```text
    Agent ID: asst_pskNeFYuoCPogDnmfaqIUwoU
    ```

## Azure AI Foundry で Agent を探索する

Azure AI Foundry には、Agentアプリと対話し、さまざまなクエリに対する応答をテストできるプレイグラウンドが含まれています。このプレイグラウンドは完全なチャットボット体験ではなく、テストツールであることに注意してください。また、Contoso 売上データベースリソースはローカルでのみ利用可能なため、リアルタイムアクセスはできません。

1.  ブラウザから [Azure AI Foundry ポータル](https://ai.azure.com/){:target="_blank"} に移動します。
2.  左側のナビゲーションから **Playgrounds** を選択します。
3.  **Try the Agents playground** を選択します。
4.  先ほどコピーした**Agent ID** を **Agent id** フィールドに貼り付けます。

### Agent の指示を確認する

`instructions_bing_grounding.txt` ファイルからの指示であることがわかります。これらの指示は、クエリに応答する際にAgentをガイドするために使用されます。

### プレイグラウンドでAgentとの会話を開始する

プレイグラウンドを使用してさまざまなクエリをテストし、Agent がどのように応答するかを観察します。ターミナルと同じクエリを再利用したり、新しいクエリを試したりできます。Agent はテントデータシートと Bing Search から情報を取得しますが、ローカルアプリのバージョンとは異なり、Contoso 売上データベースにはアクセスできないことに注意してください。
