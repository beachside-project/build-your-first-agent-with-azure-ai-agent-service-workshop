## はじめに

会話にドキュメント (ファイル) のコンテキストを含めることは非常に効果的であり、特に運用中のデータベースでは利用できない可能性のある製品詳細を取得する場合に有効です。Azure AI Agent Service には [ファイル検索ツール](https://learn.microsoft.com/en-us/azure/ai-services/agents/how-to/tools/file-search){:target="_blank"} が含まれており、これにより Agent は、ユーザーが提供したドキュメントや製品データなどのアップロードされたファイルから直接情報を取得でき、[RAG スタイル](https://learn.microsoft.com/azure/ai-studio/concepts/retrieval-augmented-generation){:target="_blank"} の検索エクスペリエンスを実現します。

このラボでは、ドキュメント検索を有効にし、Agent 用にテントのデータシートをベクトルストアにアップロードする方法を学びます。有効化されると、このツールにより Agent はファイルを検索し、関連性の高い応答を提供できるようになります。ドキュメントは、すべてのユーザー向けに Agent にアップロードしたり、特定のユーザースレッドにリンクしたり、コードインタープリターにリンクしたりできます。

アプリが起動すると、ベクトルストアが作成され、Contoso のテントデータシート PDF ファイルがベクトルストアにアップロードされ、Agent で利用可能になります。

通常、アプリが起動するたびに新しいベクトルストアを作成してドキュメントをアップロードすることはありません。代わりに、ベクトルストアを一度作成し、潜在的に数千のドキュメントをアップロードし、そのストアを Agent に接続します。

[ベクトルストア](https://en.wikipedia.org/wiki/Vector_database){:target="_blank"} は、ベクトル（テキストデータの数値表現）の保存と検索に最適化されたデータベースです。ファイル検索ツールは、アップロードされたドキュメント内の関連情報を検索するために、ベクトルストアを [セマンティック検索](https://en.wikipedia.org/wiki/Semantic_search){:target="_blank"} に使用します。

## ラボ演習

1. VS Code から **shared/datasheet/contoso-tents-datasheet.pdf** ファイルを開きます。この PDF ファイルには、Contoso が販売するテントの詳細な製品説明が含まれています。

2. Agent の応答をグラウンディングするために使用されるため、ファイルの内容を**確認**して、含まれる情報を理解します。

=== "Python"

      1. `main.py` ファイルを開きます。

      2. **"# "** 文字を削除して、次の行の**コメントを解除**します。

          ```python
          # INSTRUCTIONS_FILE = "instructions/file_search.txt"

          # vector_store = await utilities.create_vector_store(
          #     project_client,
          #     files=[TENTS_DATA_SHEET_FILE],
          #     vector_store_name="Contoso Product Information Vector Store",
          # )
          # file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
          # toolset.add(file_search_tool)
          ```

        !!! warning
            コメント解除する行は隣接していません。# 文字を削除する際は、その後のスペースも削除するようにしてください。

      3. `main.py` ファイルのコードを確認します。

          コメント解除後、コードは次のようになります：

          ```python
          INSTRUCTIONS_FILE = "instructions/function_calling.txt"
          INSTRUCTIONS_FILE = "instructions/file_search.txt"
          # INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
          # INSTRUCTIONS_FILE = "instructions/code_interpreter_multilingual.txt"
          # INSTRUCTIONS_FILE = "instructions/bing_grounding.txt"


          async def add_agent_tools() -> None:
              """Add tools for the agent."""
              font_file_info = None

              # 関数ツールを追加
              toolset.add(functions)

              # テントのデータシートを新しいベクトルデータストアに追加
              vector_store = await utilities.create_vector_store(
                  project_client,
                  files=[TENTS_DATA_SHEET_FILE],
                  vector_store_name="Contoso Product Information Vector Store",
              )
              file_search_tool = FileSearchTool(vector_store_ids=[vector_store.id])
              toolset.add(file_search_tool)

            # コードインタープリターツールを追加
            # code_interpreter = CodeInterpreterTool()
            # toolset.add(code_interpreter)

            # Bing grounding ツールを追加
            # bing_connection = await project_client.connections.get(connection_name=BING_CONNECTION_NAME)
            # bing_grounding = BingGroundingTool(connection_id=bing_connection.id)
            # toolset.add(bing_grounding)

            # コードインタープリターに多言語サポートを追加
            # font_file_info = await utilities.upload_file(project_client, utilities.shared_files_path / FONTS_ZIP)
            # code_interpreter.add_file(file_id=font_file_info.id)

            return font_file_info
          ```

=== "C#"

    1. `Program.cs` ファイルを開きます。
    2. `Lab` の作成を `Lab2` クラスを使用するように**更新**します。

        ```csharp
        await using Lab lab = new Lab2(projectClient, apiDeploymentName);
        ```

    3. `Lab2.cs` クラスを確認し、`InitialiseLabAsync` が PDF をベクトルストアに追加しファイル検索ツールを Agent に追加するためにどのように使用され、`InitialiseToolResources` がファイル検索ツールを Agent に追加するためにどのように使用されるかを確認します。これらのメソッドは、プロセスを観察するためにブレークポイントを追加するのに適した場所です。

## 関数の確認

1. **utilities.py** ファイル内の **create_vector_store** 関数を確認します。`create_vector_store` 関数は、テントのデータシートをアップロードし、ベクトルストアに保存します。

    VS Code デバッガーの使用に慣れている場合は、**create_vector_store** 関数に[ブレークポイント](https://code.visualstudio.com/Docs/editor/debugging){:target="_blank"}を設定して、ベクトルストアがどのように作成されるかを観察します。

2. **shared/instructions/file_search.txt** ファイルを開きます。"2. Tools & Data Access" セクションで更新されている内容を、前のステップで使用したものと比較して確認してみましょう。
  

## Agent App の実行

1. <kbd>F5</kbd> を押してアプリを実行します。
2. ターミナルにアプリの起動が表示され、Agent App から**クエリを入力してください (Enter your query)** というプロンプトが表示されます。

### Agent との会話を開始する

以下の会話では、Contoso 売上データベースとアップロードされたテントデータシートの両方のデータを使用するため、結果はクエリによって異なります。

1. **どのブランドのテントを販売していますか？**

    Agent は、テントデータシートに記載されている一意のテントブランドのリストを返します。

    !!! info
        Agent は提供されたデータシートを参照して、ブランド、説明、製品タイプ、カテゴリなどの詳細にアクセスし、このデータを Contoso 売上データベースに関連付けることができるようになりました。


2. **どのブランドのハイキングシューズを販売していますか？**

    !!! info
        エージェントには、ハイキングシューズに関する情報を含むファイルは提供していません。

        エージェントがそのベクトルストアから取得できない情報に関する質問をどのように扱うか観察してください。

3. **これらのブランドに関連付けられている製品タイプとカテゴリは何ですか？**

    Agent は、テントブランドに関連付けられている製品タイプとカテゴリのリストを提供します。

4. **2024年のテントの売上高は製品タイプ別にどのくらいでしたか？各製品に関連するブランドを含めてください。**

    !!! info
        Agent がこれを間違え、AlpineGear に "FAMILY CAMPING TENTS" (ファミリーキャンプ用テント) があると誤って示唆する可能性があります。これに対処するには、指示やデータシートでさらにコンテキストを提供するか、次のプロンプトのように Agent に直接コンテキストを提供します。
        Agent がこれを誤り、AlpineGearが "FAMILY CAMPING TENTS" (ファミリーキャンプ用テント)を販売していると間違って示唆する可能性があります。これに対処するには、指示またはデータシートにさらなるコンテキストを提供するか、次のプロンプトのようにエージェントに直接コンテキストを提供できます。例として、次を試してください：「Contoso は AlpineGear の FAMILY CAMPING TENTS を販売していません。もう一度確認してください。」

5. **2024年の AlpineGear の地域別売上は？**

    Agent は Contoso 売上データベースからの売上データで応答します。

    !!! info
        Agent はこれを、「CAMPING & HIKING」カテゴリ内のすべてのテントの売上を検索する要求として解釈します。これは、Agent が Alpine Gear が backpacking tent のブランドであるという情報にアクセスできるようになったためです。

6. **地域別の売上を円グラフで表示して**

    私たちのエージェントは、まだチャートを作成できません。次のラボで実施できるようになります。


## Agent Appの停止

完了したら、**exit** と入力して Agent のリソースをクリーンアップし、アプリを停止します。
