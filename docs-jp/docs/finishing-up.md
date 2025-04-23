このワークショップのラボ部分は以上です。主要なポイントと追加リソースについてはこの先をお読みください。まずは後片付けをしましょう。

## GitHub リポジトリにスターを付ける

GitHub アカウントをお持ちの場合は、このリポジトリに「スター」を付けて、将来簡単に見つけられるようにすることができます。

* GitHub リポジトリにアクセスします： [microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop](https://github.com/microsoft/build-your-first-agent-with-azure-ai-agent-service-workshop){:target="_blank"}
* GitHub アカウントにログインします
* 右上の **Star** をクリックします

将来このワークショップを再度見つけるには、右上の GitHub プロフィール写真をクリックし、**Your stars** をクリックします。

## GitHub CodeSpaces のクリーンアップ

!!! note
    このラボを実行するために GitHub Codespaces を使用しなかった場合（例えば、Microsoft AI Tour ラボなど）、このステップはスキップできます。

### GitHub に変更を保存する

ワークショップ中に行ったファイルへの変更は、フォークとして個人の GitHub リポジトリに保存できます。これにより、カスタマイズした内容でワークショップを簡単に再実行でき、ワークショップの内容は常に GitHub アカウントで利用可能になります。

  * VS Code で、左ペインの「ソース管理 (Source Control)」ツールをクリックします。上から 3 番目です。または、キーボードショートカット \<kbd\>Control-Shift-G\</kbd\> を使用することもできます。
  * 「ソース管理 (Source Control)」の下のフィールドに `Agents Lab` と入力し、**✔️コミット (Commit)** をクリックします。
      * 「コミットするステージ済みの変更はありません (There are no staged changes to commit.)」というプロンプトに **Yes** をクリックします。
  * **変更の同期 (Sync Changes)** をクリックします。
      * 「このアクションは origin/main からコミットをプルおよびプッシュします (This action will pull and push commits from and to origin/main)」というプロンプトに **OK** をクリックします。

これで、カスタマイズされたワークショップの独自のコピーが GitHub アカウントに作成されました。

### GitHub Codespace の削除

GitHub CodeSpace は自動的にシャットダウンしますが、削除されるまでコンピューティングとストレージの割り当て量を少量消費します。（使用状況は [GitHub 請求概要 (GitHub Billing summary)](https://github.com/settings/billing/summary) で確認できます。）次のようにして、Codespace を安全に削除できます：

  * [github.com/codespaces](https://github.com/codespaces){:target="\_blank"} にアクセスします
  * ページの下部で、アクティブな Codespace の右側にある「...」メニューをクリックします
  * **削除 (Delete)** をクリックします
      * 「よろしいですか？ (Are you sure?)」というプロンプトで、**削除 (Delete)** をクリックします。

## Azure リソースの削除

!!! note
ラボ提供の Azure アカウントを使用している場合は、このステップをスキップできます。ラボ管理者は、ラボ完了後すぐに一時的な Azure サブスクリプションを削除します。

このラボで作成したリソースのほとんどは従量課金制リソースであり、使用に対してこれ以上課金されることはありません。ただし、AI Foundry が使用する一部のストレージサービスでは、わずかな継続的料金が発生する場合があります。すべてのリソースを削除するには、次の手順に従います：

  * [Azure ポータル](https://portal.azure.com){:target="_blank"} にアクセスします
  * **リソース グループ**をクリックします
  * リソース グループ `rg-contoso-agent-workshop` をクリックします
  * **リソース グループの削除 (Delete Resource group)** をクリックします
  * 下部の「削除を確認するためにリソース グループ名を入力してください (Enter resource group name to confirm deletion)」フィールドに `rg-contoso-agent-workshop` と入力します
  * **削除 (Delete)** をクリックします
      * 削除確認のプロンプトで、「削除 (Delete)」をクリックします