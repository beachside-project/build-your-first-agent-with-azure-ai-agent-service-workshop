## はじめに

Azure AI Agent Service のコードインタープリターを使用すると、LLM はユーザーのクエリに基づいてグラフを作成したり、複雑なデータ分析を実行したりするタスクのために、Python コードを安全に実行できます。これは、自然言語処理 (NLP)、SQLite データベースからの売上データ、およびユーザープロンプトを使用してコード生成を自動化します。LLM によって生成された Python コードは、安全で制御された実行を保証するために、Python の制限されたサブセット上で実行される、安全なサンドボックス環境内で実行されます。

## ラボ演習 - Python

このラボでは、LLM によって生成された Python コードを実行するためにコードインタープリターを有効にします。

=== "Python"

    1. `main.py` を開きます。

    2. Agent 私たちのエージェントのために新しい指示ファイルを定義し、エージェントのツールセットにコードインタープリターを追加します。"#" 文字を削除することにより、以下の行のコメントを解除します。

        ```python
        # INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"

        # code_interpreter = CodeInterpreterTool()
        # toolset.add(code_interpreter)
        ```

        !!! warning
            コメント解除する行は隣接していません。# 文字を削除する際は、その後のスペースも削除するようにしてください。

    3. `main.py` ファイルのコードを確認します。

        コメント解除後、コードは次のようになります：

        ```python
        INSTRUCTIONS_FILE = "instructions/function_calling.txt"
        INSTRUCTIONS_FILE = "instructions/file_search.txt"
        INSTRUCTIONS_FILE = "instructions/code_interpreter.txt"
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
            code_interpreter = CodeInterpreterTool()
            toolset.add(code_interpreter)

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

    2. ラボの作成を `Lab2` クラスを使用するように**更新**します。

        ``` csharp
        await using Lab lab = new Lab3(projectClient, apiDeploymentName);
        ```

    3. `Lab2.cs` クラスを確認し、コードインタープリターがツールリストにどのように追加されるかを確認します。


## 指示の確認

1. **shared/instructions/code_interpreter.txt** ファイルを開きます。このファイルは、前のラボで使用された指示を置き換えます。
2. **ツール**セクションには、「視覚化とコード解釈 (Visualization and Code Interpretation)」機能が含まれるようになり、Agent は次のことができるようになります：

    * コードインタープリターを使用して、LLM が生成した Python コードを実行します。（例：データのダウンロードや視覚化のため）。
    * ユーザーの言語を使用して、ラベル、タイトル、その他のグラフテキストを含むチャートやグラフを作成します。
    * 視覚化を PNG ファイルとして、データを CSV ファイルとしてエクスポートします。

## Agent App の実行

1. <kbd>F5</kbd> を押してアプリを実行します。
2. ターミナルでアプリが起動し、Agent App から**クエリを入力してください (Enter your query)** というプロンプトが表示されます。

### Agent との会話を開始する

これらの質問を試してみてください：

1. **地域別売上を円グラフで表示して** (または「Show sales by region as a pie chart」など)

    タスクが完了すると、円グラフの画像が **shared/files** サブフォルダーに保存されます。このサブフォルダーは、このタスクがはじめて実行されるときに作成され、ソース管理にはチェックインされません。

    VS Code でフォルダーを開き、画像ファイルをクリックして表示します。（ヒント：Codespaces では、Agent が応答で出力するリンクを Control キーを押しながらクリックするとファイルを表示できます。）

    !!! info
        これは魔法のように感じるかもしれませんが、舞台裏では何が起こってすべてが機能しているのでしょうか？

        Azure AI Agent Service は次のステップを調整します：

        1. LLM はユーザーの質問に答えるための SQL クエリを生成します。この例では、クエリは次のとおりです：

            **SELECT region, SUM(revenue) AS total_revenue FROM sales_data GROUP BY region;**

        2. LLM は Agent app に **async_fetch_sales_data_using_sqlite_query** 関数を呼び出すよう要求します。SQL コマンドが実行され、結果のデータが LLM に返されます。
        3. 返されたデータを使用して、LLM は円グラフを作成するための Python コードを記述します。
        4. 最後に、コードインタープリターが Python コードを実行してグラフを生成します。

2. **地域別売上データをダウンロードして** (または「Download the sales by region data」など)

    タスクが完了したら、**shared/files** フォルダーを確認してダウンロードされたファイルを確認します。

    !!! info
        デフォルトでは、指示はデータが CSV 形式でダウンロードされることを指定しています。クエリに希望の形式を含めることで、JSON や Excel などの他の形式をリクエストできます（例：「JSON としてダウンロード」）。

3. **Download as JSON** (または「JSON としてダウンロード」など)

    タスクが完了したら、**shared/files** フォルダーを確認してダウンロードされたファイルを確認します。

    !!! info
        明示的に指定しなかったにもかかわらず、Agent は会話から作成したいファイルを推測しました。

4. Contoso の売上データについて質問を続け、コードインタープリターの動作を確認します。

## コードインタープリターのデバッグ

コードインタープリターを直接デバッグすることはできませんが、エージェントに生成したコードを表示するように依頼することでその挙動についての洞察を得ることができます。これは、Agent が指示をどのように解釈するかを理解し、それらを改善する際に役立ちます。

ターミナルで以下を入力します。

1. **show code** (コードを表示して) と入力して、コードインタープリターによって生成された直前の操作に対するコードを確認します。


## Agent App の停止

完了したら、**exit** と入力してAgent のリソースをクリーンアップし、アプリを停止します。
