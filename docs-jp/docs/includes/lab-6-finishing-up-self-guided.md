このワークショップのラボは以上です。主要なポイントと追加リソースについてはこの先をお読みください。まずは後片付けをしましょう。

## Clean up GitHub CodeSpaces

### GitHub に変更を保存する

ワークショップ中にファイルに行った変更は、個人の GitHub リポジトリにフォークとして保存できます。これにより、あなたのカスタマイズを適用してワークショップを簡単に再実行でき、ワークショップのコンテンツはあなたのGitHubアカウントに常に残ります。

* VS Code で、左ペインの「ソース管理 (Source Control)」ツールをクリックします。上から 3 番目です。または、キーボードショートカット <kbd>Control - Shift - G</kbd> を使用することもできます。
* 「ソース管理 (Source Control)」の下のフィールドに `Agents Lab` と入力し、**✔️コミット (Commit)** をクリックします。
  * 「コミットするステージ済みの変更はありません (There are no staged changes to commit.)」というプロンプトに **Yes** をクリックします。
* **変更の同期 (Sync Changes)** をクリックします。
  * 「このアクションは origin/main からコミットをプルおよびプッシュします (This action will pull and push commits from and to origin/main)」というプロンプトに **OK** をクリックします。

これで、カスタマイズされたワークショップの独自のコピーが GitHub アカウントに作成されました。

### GitHub Codespace の削除

GitHub CodeSpace は自動的にシャットダウンしますが、削除されるまでコンピューティングとストレージの割り当て量を少量消費します。（使用状況は [GitHub 請求概要 (GitHub Billing summary)](https://github.com/settings/billing/summary) で確認できます。）次のようにして、Codespace を安全に削除できます：

* [github.com/codespaces](https://github.com/codespaces){:target="_blank"} にアクセスします
* ページの下部で、アクティブな Codespace の右側にある「...」メニューをクリックします
* **削除 (Delete)** をクリックします
  * 「よろしいですか？ (Are you sure?)」というプロンプトで、**削除 (Delete)** をクリックします。

## Azure のリソース削除

このラボで作成したリソースのほとんどは従量課金制リソースであり、それ以上の使用に対して料金は発生しません。ただし、AI Foundryが使用する一部のストレージサービスでは、少額の継続的な料金が発生する場合があります。すべてのリソースを削除するには、以下の手順にしたがってください。

* [Azure ポータル](https://portal.azure.com){:target="_blank"} にアクセスします。
* **リソース グループ**をクリックします。
* リソース グループ `rg-contoso-agent-workshop` をクリックします。
* **リソース グループの削除 (Delete Resource group)** をクリックします。
* 下部の「削除を確認するためにリソース グループ名を入力してください (Enter resource group name to confirm deletion)」フィールドに `rg-contoso-agent-workshop` と入力します。
* **削除 (Delete)** をクリックします。
  * 削除確認のプロンプトで、「削除 (Delete)」をクリックします。
