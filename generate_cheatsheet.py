# -*- coding: utf-8 -*-
"""
CloudWatch トレースクエリ チートシート & 詳細リファレンス 生成スクリプト
AWS CloudWatch Traces (X-Ray フィルター式) および CloudWatch Logs Insights / Transaction Search
Excel (.xlsx) と Markdown (.md) を完全生成
"""

import os
import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

def build_excel_workbook(file_path):
    wb = openpyxl.Workbook()
    # Remove default sheet
    wb.remove(wb.active)

    # Styles
    FONT_FAMILY = "Meiryo UI"
    
    font_title = Font(name=FONT_FAMILY, size=15, bold=True, color="FFFFFF")
    font_subtitle = Font(name=FONT_FAMILY, size=10, italic=True, color="E0E0E0")
    font_sec = Font(name=FONT_FAMILY, size=11, bold=True, color="FFFFFF")
    font_tbl_hdr = Font(name=FONT_FAMILY, size=10, bold=True, color="FFFFFF")
    font_bold = Font(name=FONT_FAMILY, size=10, bold=True, color="212529")
    font_regular = Font(name=FONT_FAMILY, size=9.5, color="212529")
    font_code = Font(name=FONT_FAMILY, size=9, bold=True, color="1E293B")
    font_note = Font(name=FONT_FAMILY, size=9, italic=True, color="495057")

    fill_title = PatternFill(start_color="212529", end_color="212529", fill_type="solid")
    fill_sec = PatternFill(start_color="343A40", end_color="343A40", fill_type="solid")
    fill_tbl_hdr = PatternFill(start_color="2B3035", end_color="2B3035", fill_type="solid")
    fill_sub_hdr = PatternFill(start_color="495057", end_color="495057", fill_type="solid")
    fill_zebra = PatternFill(start_color="F8F9FA", end_color="F8F9FA", fill_type="solid")
    fill_code = PatternFill(start_color="F1F3F5", end_color="F1F3F5", fill_type="solid")
    fill_alert = PatternFill(start_color="E9ECEF", end_color="E9ECEF", fill_type="solid")

    border_thin = Side(border_style="thin", color="CED4DA")
    border_medium = Side(border_style="medium", color="6C757D")
    border_double = Side(border_style="double", color="343A40")

    box_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)
    hdr_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_medium)
    code_border = Border(left=border_thin, right=border_thin, top=border_thin, bottom=border_thin)

    align_center = Alignment(horizontal="center", vertical="center", wrap_text=True)
    align_left = Alignment(horizontal="left", vertical="top", wrap_text=True)
    align_code = Alignment(horizontal="left", vertical="top", wrap_text=True)

    # ----------------------------------------------------
    # Sheet 1: 01_クイックチートシート
    # ----------------------------------------------------
    ws1 = wb.create_sheet(title="01_クイックチートシート")
    ws1.views.sheetView[0].showGridLines = True

    # Title Block
    ws1.merge_cells("A1:G1")
    ws1["A1"] = "CloudWatch トレースクエリ 即実行クイックチートシート (コピペ用)"
    ws1["A1"].font = font_title
    ws1["A1"].fill = fill_title
    ws1["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[1].height = 36

    ws1.merge_cells("A2:G2")
    ws1["A2"] = "AWSマネジメントコンソールの「トレース」検索バー、または「Logs Insights」に貼り付けて「クエリを実行」を押すだけで即座に結果を取得できます。"
    ws1["A2"].font = font_subtitle
    ws1["A2"].fill = fill_title
    ws1["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws1.row_dimensions[2].height = 20

    headers_ws1 = [
        ("No", 6),
        ("カテゴリ", 16),
        ("対象画面", 18),
        ("クエリ名・ユースケース", 28),
        ("そのままコピペして実行できるクエリ", 55),
        ("動作とフィルタ内容の説明", 45),
        ("実務でのカスタマイズ例・注意点", 35)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws1, 1):
        cell = ws1.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws1.column_dimensions[col_letter].width = width

    ws1.row_dimensions[4].height = 28

    cheatsheet_data = [
        # エラーのフィルタ
        (1, "エラーのフィルタ", "CloudWatch トレース", "サーバー障害 (HTTP 5xx / 例外) 抽出",
         "fault = true",
         "サーバー側で発生した5xx系エラー（500, 502, 503, 504）や、アプリケーションクラッシュ等の未処理例外を含むトレースのみを抽出します。",
         "最も基本の障害検知クエリ。サービスマップ上で赤色表示されるノードを絞り込みます。"),
        (2, "エラーのフィルタ", "CloudWatch トレース", "クライアントエラー (HTTP 4xx) 抽出",
         "error = true",
         "クライアント起因の4xx系エラー（400 Bad Request, 401 Unauthorized, 403 Forbidden, 404 Not Found等）を抽出します。",
         "認証エラーやリクエスト不正の調査に活用。404を除外したい場合は http.status != 404 を付与。"),
        (3, "エラーのフィルタ", "CloudWatch トレース", "スロットリング (HTTP 429) 抽出",
         "throttle = true",
         "API GatewayやDynamoDB、自社APIのレート制限（HTTP 429 Too Many Requests）に抵触したリクエストのみを抽出します。",
         "突発的なアクセス集中やクォータ枯渇の調査に必須。"),
        (4, "エラーのフィルタ", "CloudWatch トレース", "全エラー統合 (4xx または 5xx)",
         "error = true OR fault = true",
         "クライアントエラーとサーバーエラーの双方を漏れなく一括抽出します。",
         "システム全体の健全性チェック、障害一次切り分け用。"),
        (5, "エラーのフィルタ", "CloudWatch トレース", "特定HTTPステータス (500 Internal Error)",
         "http.status = 500",
         "HTTPステータスコードが厳密に500番のトレースをピンポイント抽出します。",
         "502（Bad Gateway）や504（Gateway Timeout）と切り分けてバックエンド不具合を特定。"),
        (6, "エラーのフィルタ", "CloudWatch トレース", "ゲートウェイ障害 (502〜504 範囲指定)",
         "http.status BETWEEN 502 AND 504",
         "リバースプロキシやALB、API Gatewayでタイムアウトや接続切断が発生したトレースを範囲指定で抽出します。",
         "BETWEEN演算子は境界値を含みます（502, 503, 504）。"),
        (7, "エラーのフィルタ", "CloudWatch トレース", "非正常完了トレース全件",
         "!ok",
         "正常（ok）ではない全リクエスト（error, fault, throttleのいずれかを含む）をすべて抽出します。",
         "手っ取り早く何らかの異常が発生したトランザクションを一覧化する際に最適。"),

        # 時間範囲・レスポンス時間
        (8, "時間範囲・遅延", "CloudWatch トレース", "2秒以上の遅延リクエスト抽出",
         "responsetime >= 2.0",
         "全体の所要時間が2秒以上かかった遅延トランザクションを抽出します。",
         "秒単位（実数値）で指定可能。SLA/SLO（例: 2秒以内）違反のリクエストを特定。"),
        (9, "時間範囲・遅延", "CloudWatch トレース", "5秒以上の重大なボトルネック抽出",
         "responsetime > 5.0",
         "5秒を超える深刻なスロークエリや外部API待ちが発生しているトレースを抽出します。",
         "画面フリーズやユーザー離脱に直結するクリティカルパスの特定に使用。"),
        (10, "時間範囲・遅延", "CloudWatch トレース", "所要時間範囲指定 (1秒〜3秒)",
         "responsetime BETWEEN 1.0 AND 3.0",
         "レスポンスタイムが1.0秒以上かつ3.0秒以下のトランザクションを抽出します。",
         "タイムアウト寸前で踏みとどまっている「隠れた高負荷リクエスト」の調査に有効。"),
        (11, "時間範囲・遅延", "CloudWatch トレース", "遅延かつエラーの複合障害特定",
         "responsetime >= 3.0 AND fault = true",
         "3秒以上処理がかかった上に最終的に5xxエラーとなった最悪パターンのトレースを特定します。",
         "タイムアウト起因のサーバーエラーを特定する実務の鉄板クエリ。"),

        # サービス・ロググループ相関
        (12, "ログ・サービス相関", "CloudWatch トレース", "JBossEAPサービス指定",
         'service("jboss-eap-app")',
         "サービスマップ上の特定サービス名「jboss-eap-app」を経由した全トレースを抽出します。",
         "マイクロサービス群の中から自チームのJBossコンテナ/EC2に絞り込む際に使用。"),
        (13, "ログ・サービス相関", "CloudWatch トレース", "JBossEAPでのサーバーエラー限定",
         'service("jboss-eap-app") { fault = true }',
         "JBoss EAPサービスノード自体で5xxエラー（未処理例外等）を発生させたトレースのみを抽出します。",
         "他サービスのエラー波及を除外し、JBoss自身の不具合を確定させる構文。"),
        (14, "ログ・サービス相関", "CloudWatch トレース", "ALBからJBossへの通信エッジ指定",
         'edge("Frontend-ALB", "jboss-eap-app") { fault = true }',
         "フロントエンドALBとJBoss EAPの間の通信パスで発生した障害トレースを抽出します。",
         "ネットワーク層やロードバランサーのヘルスチェック切断トラブル調査に。"),

        # JBoss EAP コード
        (15, "JBoss EAPコード", "CloudWatch トレース", "管理操作失敗コード (WFLYCTL0013)",
         'annotation.errorCode = "WFLYCTL0013"',
         "JBoss EAPのWildFlyコア管理操作失敗コード「WFLYCTL0013」が記録されたトレースを抽出します。",
         "アノテーション（Annotation）としてX-Ray SDK / OpenTelemetryで付与したキーを検索。"),
        (16, "JBoss EAPコード", "CloudWatch トレース", "DBプール枯渇 (IJ000453)",
         'annotation.errorCode = "IJ000453"',
         "IronJacamar（JCAデータソース）のコネクション取得失敗・プール枯渇エラーを抽出します。",
         "JBoss EAPで最も頻発するDB接続枯渇トラブルを即座に検知。"),
        (17, "JBoss EAPコード", "CloudWatch トレース", "WFLYで始まる全コード前方一致",
         'annotation.errorCode STARTSWITH "WFLY"',
         "WFLY（WildFly/JBoss EAP）で始まるすべてのサブシステムエラーコードを前方一致で抽出します。",
         "STARTSWITH演算子でJBoss固有エラーを網羅的に洗い出し。"),

        # Java エラーメッセージ
        (18, "Javaエラー", "CloudWatch トレース", "NullPointerException (NPE) 抽出",
         'annotation.exception CONTAINS "NullPointerException"',
         "例外メッセージやクラス名に「NullPointerException」を含むトレースを抽出します。",
         "CONTAINS演算子は部分一致。Javaで最も多い参照エラーの追跡用。"),
        (19, "Javaエラー", "CloudWatch トレース", "SQLException (DB例外) 抽出",
         'annotation.exception CONTAINS "SQLException"',
         "SQL文の構文エラーやタイムアウト、制約違反などのDB例外を包括的に抽出します。",
         "データベース接続不良やデッドロック調査に直結。"),
        (20, "Javaエラー", "CloudWatch トレース", "OutOfMemoryError (メモリ枯渇)",
         'annotation.exception CONTAINS "OutOfMemoryError"',
         "Javaヒープやメタスペースのメモリ枯渇（OOM）が発生した重大インシデントを抽出します。",
         "プロセス再起動やヒープダンプ採取が必要な緊急事態を特定。"),
        (21, "Javaエラー", "CloudWatch トレース", "TimeoutException (タイムアウト)",
         'annotation.exception CONTAINS "TimeoutException"',
         "非同期処理や外部マイクロサービス通信でのタイムアウト例外を抽出します。",
         "外部APIの遅延に引きずられて発生した障害の究明に利用。"),

        # 文字列除外
        (22, "文字列除外", "CloudWatch トレース", "ヘルスチェックURLの完全除外",
         '!http.url CONTAINS "health"',
         "URLパスに「health」（例: /health, /healthcheck, /actuator/health）を含む監視リクエストを除外します。",
         "「!」演算子で否定。ログの大半を占める死活監視ノイズを一掃。"),
        (23, "文字列除外", "CloudWatch トレース", "ALBヘルスチェッカーUAの除外",
         'NOT http.user_agent CONTAINS "ELB-HealthChecker"',
         "AWS ALBのヘルスチェッカー（ELB-HealthChecker）からの自動リクエストを除外します。",
         "「NOT」キーワードも使用可能。一般ユーザーからのリクエストのみに絞り込み。"),
        (24, "文字列除外", "CloudWatch トレース", "CORS OPTIONSプリフライト除外",
         'http.method != "OPTIONS"',
         "ブラウザが自動送信するCORSプリフライト（OPTIONSメソッド）を除外します。",
         "純粋な業務APIリクエスト（GET, POST, PUT, DELETE）のみを分析対象に。"),
        (25, "文字列除外", "CloudWatch トレース", "障害のみ抽出＋ヘルスチェック除外 (実務鉄板)",
         'fault = true AND !http.url CONTAINS "health"',
         "ヘルスチェックを完全に除外した上で、本番ユーザー向けリクエストの5xx障害のみを抽出します。",
         "本番障害アラート発生時にまず最初に実行すべき鉄板クエリ。"),

        # Logs Insights / Transaction Search
        (26, "Logs Insights", "Logs Insights", "JBossエラーログからTraceIDと例外抽出",
         "fields @timestamp, @logStream, @message\n| filter @message like /ERROR/ or @message like /WFLY/\n| filter @message not like /healthcheck/\n| sort @timestamp desc\n| limit 100",
         "JBoss EAPのserver.logからエラーやWFLYコードを含み、ヘルスチェックを除外したログを降順取得します。",
         "CloudWatch Logs Insights画面で対象ロググループ（/aws/ecs/jboss等）を選択して実行。"),
        (27, "Logs Insights", "Logs Insights", "Java NPEとスタックトレースCaused by特定",
         "fields @timestamp, @message\n| filter @message like /NullPointerException/ or @message like /Caused by:/\n| sort @timestamp desc\n| limit 50",
         "JavaのNullPointerExceptionおよび根本原因を示す「Caused by:」行を抽出します。",
         "ネストされた長い例外スタックトレースから真の原因を素早く炙り出します。"),
        (28, "Logs Insights", "Logs Insights", "JBoss DBコネクション枯渇ログ特定",
         "fields @timestamp, @message\n| filter @message like /IJ000453/ or @message like /IJ000655/\n| sort @timestamp desc\n| limit 50",
         "IronJacamarのコネクション枯渇メッセージ（IJ000453/IJ000655）を直接検索します。",
         "DB接続プール溢れの発生時刻と頻度を正確に把握可能。"),
        (29, "Logs Insights", "Logs Insights", "トランザクション検索 (/aws/spans) エラー分析",
         "fields @timestamp, traceId, serviceName, name, duration, status.code\n| filter status.code = \"ERROR\" or duration > 2000\n| sort duration desc\n| limit 50",
         "CloudWatch Transaction Searchの「/aws/spans」ロググループから、エラーまたは2秒以上遅延したスパンを降順取得します。",
         "OpenTelemetry/X-Ray連携の現代的トランザクション検索クエリ。"),
        (30, "Logs Insights", "Logs Insights", "特定TraceIDに紐づく全ログの串刺し抽出",
         "fields @timestamp, @log, @message\n| filter @message like /1-670dcba0-123456789abcdef012345678/\n| sort @timestamp asc",
         "特定トレースIDがログに出力されている場合、複数ロググループをまたいでリクエストの一連ログを時系列で復元します。",
         "トレース画面で見つけた問題のTrace IDを貼り付けて、詳細ログを完全追跡。")
    ]

    for row_idx, rdata in enumerate(cheatsheet_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws1.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 5 else font_regular
            cell.fill = fill_code if col_idx == 5 else (row_fill if row_fill else PatternFill(fill_type=None))
            cell.alignment = align_code if col_idx == 5 else (align_center if col_idx in [1, 3] else align_left)
            cell.border = code_border if col_idx == 5 else box_border
            
        ws1.row_dimensions[row_idx].height = 42 if "\n" in str(rdata[4]) else 28

    ws1.freeze_panes = "D5"
    ws1.auto_filter.ref = f"A4:G{len(cheatsheet_data) + 4}"

    print("Sheet 1 generated.")

    # ----------------------------------------------------
    # Sheet 2: 02_トレース検索式完全リファレンス
    # ----------------------------------------------------
    ws2 = wb.create_sheet(title="02_トレース検索式完全リファレンス")
    ws2.views.sheetView[0].showGridLines = True

    ws2.merge_cells("A1:F1")
    ws2["A1"] = "CloudWatch Traces (AWS X-Ray) フィルター式 完全構文リファレンス"
    ws2["A1"].font = font_title
    ws2["A1"].fill = fill_title
    ws2["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[1].height = 36

    ws2.merge_cells("A2:F2")
    ws2["A2"] = "CloudWatchコンソール「トレース」検索バーで使用できるすべての構文規則、演算子、予約語、実例の体系的解説です。"
    ws2["A2"].font = font_subtitle
    ws2["A2"].fill = fill_title
    ws2["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws2.row_dimensions[2].height = 20

    headers_ws2 = [
        ("分類", 18),
        ("キーワード / 構文要素", 25),
        ("型 / 演算子", 20),
        ("クエリ構文の記述例", 45),
        ("動作・判定条件の詳細", 50),
        ("実務での利用ポイント・注意点", 35)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws2, 1):
        cell = ws2.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws2.column_dimensions[col_letter].width = width

    ws2.row_dimensions[4].height = 28

    syntax_data = [
        # ブールキーワード
        ("ブールキーワード", "fault", "Boolean (=, !=, !, 単体)", "fault = true\nfault\n!fault",
         "HTTPステータス5xx系またはサーバー例外が発生したトレースを判定します。「fault」単体で真、「!fault」で偽を表せます。",
         "サーバー側のバグやダウンタイム検知に最優先で使用。"),
        ("ブールキーワード", "error", "Boolean (=, !=, !, 単体)", "error = true\nerror\n!error",
         "HTTPステータス4xx系（クライアントエラー）が発生したトレースを判定します。",
         "認証不備やリクエストパラメーター異常を捉えます。"),
        ("ブールキーワード", "throttle", "Boolean (=, !=, !, 単体)", "throttle = true\nthrottle",
         "リクエストがスロットリング（レート制限、HTTP 429）されたトレースを判定します。",
         "クォータ超過やスパイクアクセスの解析に必須。"),
        ("ブールキーワード", "ok", "Boolean (=, !=, !, 単体)", "ok = true\n!ok",
         "エラー、障害、スロットリングのいずれも発生しなかった正常完了トレースを判定します。",
         "正常系のみのパフォーマンス測定やレイテンシー比較に有効。"),
        ("ブールキーワード", "hasExpired", "Boolean (=, !=)", "hasExpired = true",
         "セグメントの一部がタイムアウト等で未完了のまま終了したトレースを判定します。",
         "非同期処理やストリーミングの途中切断調査に利用。"),

        # 数値キーワード
        ("数値キーワード", "responsetime", "Number (=, !=, <, <=, >, >=, BETWEEN)", "responsetime >= 2.5\nresponsetime BETWEEN 1.0 AND 3.0",
         "リクエストの開始から全サブセグメント完了までの合計所要時間（秒）を数値比較します。",
         "単位は「秒」です。小数点指定（例: 0.25）が可能。ミリ秒ではない点に注意。"),
        ("数値キーワード", "http.status", "Number (=, !=, <, <=, >, >=, BETWEEN)", "http.status = 500\nhttp.status >= 400",
         "HTTPレスポンスのステータスコードを比較します。",
         "APIやマイクロサービス間のステータスコードベースのフィルタに最適。"),

        # 文字列キーワード
        ("文字列キーワード", "http.url", "String (=, !=, CONTAINS, STARTSWITH, ワイルドカード)", 'http.url CONTAINS "/api/order"\nhttp.url = "*/checkout*"',
         "リクエスト先のURL文字列を比較します。アスタリスク(*)やクエスチョンマーク(?)によるワイルドカード一致もサポート。",
         "特定のAPIエンドポイントへのアクセスに絞り込む際に多用。"),
        ("文字列キーワード", "http.method", "String (=, !=)", 'http.method = "POST"\nhttp.method != "GET"',
         "HTTPメソッド（GET, POST, PUT, DELETE, OPTIONS, HEAD等）を指定します。",
         "データ更新リクエスト（POST/PUT）のみの遅延調査に有効。"),
        ("文字列キーワード", "http.user_agent", "String (=, !=, CONTAINS)", 'http.user_agent CONTAINS "Mobile"\nNOT http.user_agent CONTAINS "ELB"',
         "クライアントのUser-Agentヘッダーを検索します。",
         "ヘルスチェッカー除外や特定クラスタ・モバイル端末起因の問題切り分けに活用。"),
        ("文字列キーワード", "http.client_ip", "String (=, !=)", 'http.client_ip = "192.168.1.100"',
         "リクエスト元のIPアドレスを指定してトレースを検索します。",
         "特定拠点やテスト端末からのトラフィック抽出に有効。"),
        ("文字列キーワード", "user", "String (=, !=)", 'user = "user-12345"',
         "X-Ray SDK等でリクエストに紐づけたユーザーIDを検索します。",
         "特定顧客の「画面が遅い」「エラーが出る」クレームのピンポイント調査に威力。"),

        # サービス・エッジ構文
        ("スコープキーワード", "service()", "スコープ関数 { 条件式 }", 'service("JBoss-EAP")\nservice("JBoss-EAP") { fault = true }',
         "指定したサービス名（X-Rayセグメント名）を通過したトレースを絞り込みます。中括弧内に条件を記述するとそのサービス内でのみ条件評価されます。",
         "マイクロサービスアーキテクチャで「自サービスの過失」を切り分ける基本テクニック。"),
        ("スコープキーワード", "edge()", "スコープ関数 { 条件式 }", 'edge("Client", "JBoss-EAP")\nedge("JBoss-EAP", "MySQL") { fault = true }',
         "2つのノード間の通信パス（エッジ）を指定します。呼び出し元サービス名と呼び出し先サービス名をカンマ区切りで指定。",
         "JBossとデータベース間の通信エラー、外部決済ゲートウェイとの通信不良を直接特定。"),

        # アノテーション
        ("アノテーション", "annotation.key", "カスタムKey-Value (String, Number, Boolean)", 'annotation.errorCode = "WFLYCTL0013"\nannotation.tenantId = 99',
         "ソースコード内でX-Ray SDKやOpenTelemetryを通じて付加された検索用インデックス（Annotation）を検索します。",
         "「アノテーション」はインデックス化されるため検索可能ですが、「メタデータ」は検索不可である点に注意。"),

        # 論理演算子・結合
        ("論理演算子", "AND (&&)", "論理積", "fault = true AND responsetime > 2.0",
         "両方の条件が同時に真であるトレースを抽出します。",
         "条件の掛け合わせで使用。"),
        ("論理演算子", "OR (||)", "論理和", "http.status = 500 OR http.status = 503",
         "いずれかの条件が真であるトレースを抽出します。",
         "複数エラー種別の統合抽出に使用。"),
        ("論理演算子", "NOT (!)", "論理否定", "!http.url CONTAINS \"health\"\nNOT error",
         "条件が偽であるトレース（条件に合致しないもの）を抽出します。",
         "ノイズ除外、ヘルスチェック除外に極めて重要。"),
        ("論理演算子", "括弧 ( )", "優先順位変更", '(error = true OR fault = true) AND !http.url CONTAINS "ping"',
         "演算子の優先順位を明示し、複雑な条件式を正確に組み立てます。",
         "ANDとORが混在する場合は必ず括弧で囲むことがベストプラクティス。")
    ]

    for row_idx, rdata in enumerate(syntax_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws2.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 4 else font_regular
            cell.fill = fill_code if col_idx == 4 else (row_fill if row_fill else PatternFill(fill_type=None))
            cell.alignment = align_code if col_idx == 4 else (align_center if col_idx in [1, 3] else align_left)
            cell.border = code_border if col_idx == 4 else box_border
            
        ws2.row_dimensions[row_idx].height = 36 if "\n" in str(rdata[3]) else 28

    ws2.freeze_panes = "D5"
    ws2.auto_filter.ref = f"A4:F{len(syntax_data) + 4}"

    print("Sheet 2 generated.")

    # ----------------------------------------------------
    # Sheet 3: 03_LogsInsights相関クエリ
    # ----------------------------------------------------
    ws3 = wb.create_sheet(title="03_LogsInsights相関クエリ")
    ws3.views.sheetView[0].showGridLines = True

    ws3.merge_cells("A1:F1")
    ws3["A1"] = "CloudWatch Logs Insights ＆ トランザクション検索 相関クエリ集"
    ws3["A1"].font = font_title
    ws3["A1"].fill = fill_title
    ws3["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[1].height = 36

    ws3.merge_cells("A2:F2")
    ws3["A2"] = "JBoss EAPのアプリケーションログ（server.log）やスパンログ（/aws/spans）を横断し、トレースとログを完全連動させる実践クエリです。"
    ws3["A2"].font = font_subtitle
    ws3["A2"].fill = fill_title
    ws3["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws3.row_dimensions[2].height = 20

    headers_ws3 = [
        ("No", 6),
        ("目的・シナリオ", 25),
        ("対象ロググループ例", 24),
        ("Logs Insights クエリ (コピペ用)", 55),
        ("クエリの構造・動作原理", 45),
        ("現場でのTips・パフォーマンス最適化", 35)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws3, 1):
        cell = ws3.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws3.column_dimensions[col_letter].width = width

    ws3.row_dimensions[4].height = 28

    logs_data = [
        (1, "JBoss エラー全件抽出 (ノイズ除外)",
         "/aws/ecs/jboss-eap\n/aws/ec2/jboss-eap",
         "fields @timestamp, @logStream, @message\n| filter @message like /ERROR/ or @message like /FATAL/\n| filter @message not like /healthcheck/\n| filter @message not like /ELB-HealthChecker/\n| sort @timestamp desc\n| limit 100",
         "ERRORまたはFATALログを抽出し、死活監視のアクセスログをnot likeで徹底排除します。",
         "時間範囲を絞るとスキャンバイト数が減り、クエリ実行時間が大幅短縮されます。"),
        (2, "JBoss サブシステムコード別集計ランキング",
         "/aws/ecs/jboss-eap",
         "fields @timestamp, @message\n| parse @message /(?<jbossCode>[A-Z]{2,7}[0-9]{4,6})/\n| filter ispresent(jbossCode)\n| stats count(*) as errorCount by jbossCode\n| sort errorCount desc\n| limit 20",
         "正規表現でWFLYCTL..., IJ..., UT...などのJBossエラーコードをパースし、発生頻度順に集計します。",
         "どのサブシステム（DB、HTTP、デプロイ等）で最も多くのエラーが噴出しているか即座に可視化。"),
        (3, "Java NPEとCaused byスタックトレース追跡",
         "/aws/ecs/jboss-eap",
         "fields @timestamp, @message\n| filter @message like /NullPointerException/ or @message like /Caused by:/\n| sort @timestamp desc\n| limit 50",
         "Javaで頻発するNullPointerExceptionと、例外チェーンの根本原因を示すCaused by行を抽出。",
         "スタックトレースが複数行に分かれている場合でも、重要行を確実にヒットさせます。"),
        (4, "IronJacamar DBコネクションプール枯渇の検出",
         "/aws/ecs/jboss-eap",
         "fields @timestamp, @message\n| filter @message like /IJ000453/ or @message like /IJ000655/\n| sort @timestamp desc\n| limit 50",
         "IronJacamarの代表的枯渇エラー「IJ000453: Unable to get managed connection」を集中的に監視。",
         "DBの最大接続数設定不足、またはトランザクション終了時のコネクションClose漏れ（リーク）の証明に。"),
        (5, "Undertow HTTPタイムアウト・通信切断",
         "/aws/ecs/jboss-eap",
         "fields @timestamp, @message\n| filter @message like /UT005023/ or @message like /UT000020/\n| sort @timestamp desc\n| limit 50",
         "JBoss EAPのWebサーバー（Undertow）でリクエスト処理中にクライアント切断やタイムアウトしたログを抽出。",
         "フロントエンドからのキャンセルやネットワーク瞬断の影響度を測定できます。"),
        (6, "トランザクション検索 (/aws/spans) エラー特定",
         "/aws/spans",
         "fields @timestamp, traceId, serviceName, name, duration, status.code\n| filter status.code = \"ERROR\"\n| sort @timestamp desc\n| limit 50",
         "OpenTelemetry/ADOTがCloudWatchの/aws/spansに出力したスパンログから、ERRORステータスのものを即座に一覧化。",
         "Modern CloudWatchの標準トレーシング検索手法。ここからTrace IDを取得してX-Rayへ遷移。"),
        (7, "トランザクション検索 (/aws/spans) スロークエリ特定",
         "/aws/spans",
         "fields @timestamp, serviceName, name, duration, traceId\n| filter duration > 2000\n| sort duration desc\n| limit 50",
         "2000ミリ秒（2秒）以上を要した重たいAPIスパンやDBクエリスパンを処理時間降順でリスト化。",
         "durationカラムはミリ秒単位。最も遅いボトルネック処理を即座に特定。"),
        (8, "パーセンタイル遅延分析 (P50, P90, P99)",
         "/aws/spans",
         "stats count(*) as totalCalls, avg(duration) as avgLatency, pct(duration, 50) as p50, pct(duration, 90) as p90, pct(duration, 99) as p99 by name\n| sort p99 desc\n| limit 20",
         "エンドポイントごとにリクエスト件数、平均遅延、P50/P90/P99レイテンシーを統計計算します。",
         "外れ値やテールレイテンシー（Tail Latency）の悪化を定量評価するSRE定番クエリ。"),
        (9, "ログ中のTrace IDによる特定リクエスト全ログ抽出",
         "複数ロググループ\n(JBoss, ALB, Microservices)",
         "fields @timestamp, @log, @message\n| filter @message like /1-670dcba0-123456789abcdef012345678/\n| sort @timestamp asc",
         "特定Trace IDをログメッセージ内から全文検索し、全コンテナ・全サービスのログを時系列で復元。",
         "Trace IDがログに含まれている（MDC等で出力設定されている）場合に威力を発揮。"),
        (10, "未処理例外とエラー発生件数の分単位推移",
         "/aws/ecs/jboss-eap",
         "filter @message like /Exception/ or @message like /ERROR/\n| stats count(*) as errorCount by bin(1m)\n| sort bin(1m) asc",
         "1分刻み（bin(1m)）でエラー発生件数を時系列カウントし、棒グラフや折れ線で可視化します。",
         "障害の発生開始時刻、ピーク時刻、収束時刻のタイムラインを客観的に把握。")
    ]

    for row_idx, rdata in enumerate(logs_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws3.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 4 else font_regular
            cell.fill = fill_code if col_idx == 4 else (row_fill if row_fill else PatternFill(fill_type=None))
            cell.alignment = align_code if col_idx == 4 else (align_center if col_idx in [1] else align_left)
            cell.border = code_border if col_idx == 4 else box_border
            
        ws3.row_dimensions[row_idx].height = 55 if "\n" in str(rdata[3]) else 28

    ws3.freeze_panes = "D5"
    ws3.auto_filter.ref = f"A4:F{len(logs_data) + 4}"

    print("Sheet 3 generated.")

    # ----------------------------------------------------
    # Sheet 4: 04_動作原理と歴史背景_小学生解説
    # ----------------------------------------------------
    ws4 = wb.create_sheet(title="04_動作原理と歴史背景_小学生解説")
    ws4.views.sheetView[0].showGridLines = True

    ws4.merge_cells("A1:E1")
    ws4["A1"] = "分散トレーシングの動作原理・歴史的背景・小学生にもわかる解説"
    ws4["A1"].font = font_title
    ws4["A1"].fill = fill_title
    ws4["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[1].height = 36

    ws4.merge_cells("A2:E2")
    ws4["A2"] = "なぜトレースクエリが必要になったのか？ その誕生の歴史と、分散システムの内部動作メカニズムを直感的に解き明かします。"
    ws4["A2"].font = font_subtitle
    ws4["A2"].fill = fill_title
    ws4["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws4.row_dimensions[2].height = 20

    headers_ws4 = [
        ("大項目", 18),
        ("中項目・テーマ", 24),
        ("小学生にもわかる解説・直感イメージ", 45),
        ("技術的な動作原理・アーキテクチャ詳細", 55),
        ("最新動向・重要ポイント", 30)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws4, 1):
        cell = ws4.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws4.column_dimensions[col_letter].width = width

    ws4.row_dimensions[4].height = 28

    theory_data = [
        # 小学生向け例え話
        ("直感的イメージ", "たとえ話①：宅配便の追跡伝票",
         "【Amazonで注文した荷物の旅】\n荷物にバーコードシール（Trace ID）が貼られます。集荷所（ALB）→ 大型倉庫（JBoss）→ 配達センター（DB）を通過するたびに『ピッ』と読み取ります（Span）。\n荷物が途中で遅れたり壊れたりしたら、伝票番号を検索するだけで『どの倉庫で何時間止まっていたか』が誰でも一瞬でわかります！",
         "リクエストがシステムに入った瞬間に一意なID（Trace ID: 例 1-5759e988-bd862e3fe1be46a994272793）を採番。各サービスがHTTPヘッダー経由でこのIDを引き継ぎ（コンテキスト伝播）、自サービス内の処理単位ごとにスパン（Span ID）を記録してAWS X-Ray / CloudWatchに非同期送信します。",
         "W3C TraceContext標準（traceparentヘッダー）として世界共通規格化。"),

        ("直感的イメージ", "たとえ話②：運動会の全員リレー",
         "【クラス全員でバトンを渡すリレー】\n第1走者（Web画面）から第2走者（JBossサーバー）、第3走者（データベース）へと『バトン（トレースヘッダー）』を渡します。\nもしゴールでタイムが遅かったり途中で転んだりしても、先生のストップウォッチ記録（トレース）を見れば、『誰が走るのに時間がかかったか』『誰がバトンを落としたか』がすぐに突き止められます！",
         "1つのトランザクションが複数サービスを巡回する際、各区間の処理時間（レイテンシー）と結果（成功/エラー）を有向非巡回グラフ（DAG）として記録。タイムライン表示によって、全体遅延のどの割合がどのサービスに起因するかをパーセンテージで可視化します。",
         "ボトルネック箇所の特定（Critical Path Analysis）が自動化。"),

        ("直感的イメージ", "たとえ話③：病院の総合カルテ",
         "【大きな病院での検査ツアー】\n受付で患者さんに1冊のカルテ（Trace ID）が渡されます。内科（JBoss）→ レントゲン室（外部API）→ 薬局（DB）と回るたびに、お医者さんが『所見や検査結果（Annotation）』をカルテに書き込みます。\n後からカルテ番号を調べれば、どこの診察室でどんな異常が見つかったのか全員が把握できます！",
         "アプリケーション内の重要変数（エラーコード、ユーザー種別、注文ID等）を「アノテーション（Annotation）」としてスパンに注入。これにより、CloudWatchの検索バーから「annotation.errorCode = ...」というクエリで瞬時に該当カルテ（トレース）を引き抜くことが可能になります。",
         "検索用インデックスが付与されるため、高速検索が可能。"),

        # 歴史と背景
        ("歴史と背景", "第1世代：モノリス時代 (1990s〜2000s)",
         "【昔は1つの大きな部屋で全員が働いていた】\n昔のシステムは、1台の大きなJBossサーバーの中に全部のプログラムが入っていました。何か失敗したら、その部屋に置いてある1冊の日記帳（server.log）を読めば、全部書いてあったので簡単でした。",
         "オンプレミスの単一アプリケーションサーバー（JBoss EAP, WebLogic, Tomcat）時代。モノリシックアーキテクチャでは、リクエストは同一JVM内のローカルスレッドで完結するため、単一のログファイルをgrepするだけで障害調査が完結していました。",
         "grepコマンドで完結した古き良き時代。"),

        ("歴史と背景", "第2世代：マイクロサービスの爆発と暗黒期 (2010s前半)",
         "【会社が急成長して20のビルに分かれた大混乱】\nシステムが便利になるにつれ、部屋が数十個の別々のビル（コンテナやAWSサービス）に分かれました。ボタンを1回押すと、20のビルに伝言が飛び交います。\nエラーが起きた時、『どのビルで誰がミスしたのか分からない！』というパニックが世界中で起きました。",
         "AWSの普及、Dockerコンテナ、マイクロサービス化の進展に伴い、1つのHTTPリクエストが内部で多数のRPCやREST API呼び出しを連鎖させる形態へ変化。ログが数十〜数百台のサーバーに散乱し、「どのログとどのログが同一トランザクションか」が追跡不能になり、MTTR（平均復旧時間）が劇的に悪化しました。",
         "「分散トレーシングがないマイクロサービスは盲目である」と言われた時代。"),

        ("歴史と背景", "第3世代：Google Dapper論文の衝撃 (2010年)",
         "【世界一頭のいい探偵が発明した解決策】\nGoogleのエンジニアが『手紙のすべてに同じスタンプ（ID）を押して、みんなで記録を残せば絶対に迷子にならない』という素晴らしい論文を発表し、世界中の基準になりました。",
         "2010年にGoogleが発表した論文『Dapper, a Large-Scale Distributed Systems Tracing Infrastructure』。分散トレーシングの基本概念（Trace, Span, Context Propagation, Out-of-band Ingestion）を体系化し、TwitterのZipkin、UberのJaegerなどオープンソースの基盤となりました。",
         "分散トレーシングのバイブル的論文。"),

        ("歴史と背景", "第4世代：AWS X-Ray の登場 (2017年)",
         "【AWS専用の超強力な追跡カメラが登場】\nAmazonがAWSを使うみんなのために、ボタンひとつで荷物の通り道（ALBやサーバー）を自動で見守ってくれる専用ツール『X-Ray』を完成させました。",
         "2016年re:Invent発表、2017年GA。AWSネイティブの分散トレーシングサービスとして、ALB、API Gateway、Lambda、ECS、DynamoDB等と深く統合。フィルター式（Filter Expression）による高速なトレース検索とサービスマップ可視化が標準機能となりました。",
         "サーバーレスやECSの可視化が飛躍的に容易に。"),

        ("歴史と背景", "第5世代：OpenTelemetryと現代のCloudWatch (2020s〜現在)",
         "【世界中の道具がひとつに大合体！】\n色々な会社が作っていた追跡ツールが世界標準ルール（OpenTelemetry）に合体。CloudWatchも進化して、ログもトレースもメトリクスも1つの画面で全部つながる最高の司令室になりました。",
         "CNCFのOpenTelemetry（OTel）が業界標準となり、AWSも「AWS Distro for OpenTelemetry (ADOT)」を提供。CloudWatch Transaction Searchにより、トレースは「/aws/spans」ロググループに集約され、Logs Insightsの超強力なパイプラインクエリ言語でトレースを自在にスキャンできるようになりました。",
         "ログ・トレース・メトリクスが完全融合（Three Pillars of Observability）。"),

        # 動作原理の深堀り
        ("動作原理", "コンテキスト伝播 (Context Propagation)",
         "【駅伝のバトンに書かれた秘密の暗号】\nランナーがバトンを渡す時、バトンに『私は誰からバトンを受け取ったか』が書いてあります。次の人はその記録を見て自分の名前を書き足して次の人に渡します。",
         "HTTP通信境界を越える際、上流サービスは下流サービスへHTTPヘッダーとしてTraceコンテキストを注入（Inject）。下流はそれを取り出し（Extract）、自身をChild SpanとしてParent Span IDを設定。これにより分散ネットワーク全体の呼び出しツリーが正確に構築されます。",
         "X-Amzn-Trace-Id形式またはW3C traceparent形式が使用される。"),

        ("動作原理", "サンプリング機構 (Sampling Rate)",
         "【全員の写真を撮るとカメラのフィルムが足りない】\n1秒間に10万人の人が走ってきたら、全員の記録を取ると先生がパンクしてしまいます。そこで『毎秒最初の1人と、あとは20人に1人だけ記録する』というルールを作って、機械が壊れないようにします。",
         "全トランザクションを100%トレースするとネットワーク帯域・ストレージ・コストが圧迫されるため、「リザーバー（毎秒固定件数保証）」＋「固定レート（例: 5%）」でサンプリングを実施。エラーが発生したトレースは優先的に保持するアダプティブサンプリングも採用されます。",
         "コストと精度のトレードオフを最適化する重要技術。"),

        ("動作原理", "アノテーション vs メタデータ の違い",
         "【図書カードに書く文字と、本の裏の落書きの違い】\n図書館で本を探す時、図書カードに書いてある『本の名前や著者名（アノテーション）』はパソコンで一瞬で検索できます。でも本の余白に書いた『メモ（メタデータ）』は、本を直接開くまで見つけられません。",
         "AWS X-Ray / CloudWatch Tracesにおいて：\n・Annotation（アノテーション）: 最大50個まで設定可能。インデックス化され、フィルター式（annotation.key = ...）で高速検索が可能。\n・Metadata（メタデータ）: 検索インデックスなし。任意の大きなJSONを保持可能で、トレース詳細画面でのみ確認可能。",
         "JBossエラーコードや重要属性は必ず「Annotation」として登録する必要がある。"),

        ("動作原理", "クエリエンジンのスキャン機構と時間パーティション",
         "【図書館の棚が『日付順』にきれいに並んでいる理由】\n探偵が『今日起きた事件』を探す時、100年前の棚まで探したら日が暮れてしまいます。『今日の棚』だけ見れば、1秒で犯人の足跡が見つかります。",
         "CloudWatchおよびLogs Insightsのストレージエンジンは、時間範囲（Timestamp）でパーティショニングされています。クエリ実行時に「過去15分」「過去1時間」といった時間枠を指定することで、走査対象のデータブロックを物理的に限定し、ミリ秒〜数秒での爆速検索を実現しています。",
         "クエリを速く・安くする鉄則は「時間範囲を必要最小限に絞ること」。")
    ]

    for row_idx, rdata in enumerate(theory_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws4.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 4 and "Trace ID:" in str(val) else font_regular
            cell.fill = row_fill if row_fill else PatternFill(fill_type=None)
            cell.alignment = align_left if col_idx >= 3 else align_center
            cell.border = box_border
            
        ws4.row_dimensions[row_idx].height = 68 if col_idx >= 3 else 32

    ws4.freeze_panes = "C5"
    ws4.auto_filter.ref = f"A4:E{len(theory_data) + 4}"

    print("Sheet 4 generated.")

    # ----------------------------------------------------
    # Sheet 5: 05_JBossEAP_Java実戦逆引き
    # ----------------------------------------------------
    ws5 = wb.create_sheet(title="05_JBossEAP_Java実戦逆引き")
    ws5.views.sheetView[0].showGridLines = True

    ws5.merge_cells("A1:F1")
    ws5["A1"] = "JBoss EAP ＆ Java 本番トラブルシューティング 実戦逆引き集"
    ws5["A1"].font = font_title
    ws5["A1"].fill = fill_title
    ws5["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[1].height = 36

    ws5.merge_cells("A2:F2")
    ws5["A2"] = "JBoss EAP 7/8で頻発するサブシステムエラーコード、主要Java例外、ノイズ除外の鉄板レシピと即効復旧ガイドです。"
    ws5["A2"].font = font_subtitle
    ws5["A2"].fill = fill_title
    ws5["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws5.row_dimensions[2].height = 20

    headers_ws5 = [
        ("障害カテゴリ", 16),
        ("エラーコード / 例外クラス", 24),
        ("発生原因と症状のメカニズム", 40),
        ("トレース・ログ特定クエリ (コピペ用)", 52),
        ("根本対策・推奨復旧アクション", 40),
        ("ノイズ除外・絞り込みの注意点", 28)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws5, 1):
        cell = ws5.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws5.column_dimensions[col_letter].width = width

    ws5.row_dimensions[4].height = 28

    troubleshooting_data = [
        # DB接続・コネクションプール
        ("DB接続・プール", "IJ000453\n(IronJacamar)",
         "【症状】Unable to get managed connection for...\nデータソースのコネクションプールが上限に達し、新しいリクエストがコネクションを取得できずタイムアウト。",
         'annotation.errorCode = "IJ000453"\nまたは Logs Insights:\nfilter @message like /IJ000453/',
         "1. standalone.xml等の max-pool-size 設定値の引き上げ。\n2. アプリケーションコードで Connection.close() や try-with-resources の漏れがないか調査。\n3. リーク検知有効化 (leak-detection-threshold)。",
         "一時的なスパイクか定常的なリークかを時系列件数推移で判別すること。"),
        ("DB接続・プール", "IJ000655\n(IronJacamar)",
         "【症状】No managed connections available within configured blocking timeout.\nブロッキングタイムアウト時間内にプールから接続が返却されず待機が力尽きた状態。",
         'annotation.errorCode = "IJ000655"\nまたは Logs Insights:\nfilter @message like /IJ000655/',
         "1. blocking-timeout-millis のチューニング。\n2. 実行中のスロークエリ特定（DB側で長時間ロックを保持しているトランザクションをキル）。",
         "スロークエリトレース（responsetime > 5.0）とセットで調査。"),

        # デプロイ・サーバー管理
        ("デプロイ・管理", "WFLYCTL0013\n(WildFly Controller)",
         "【症状】Operation failed...\nCLI管理コマンド実行時やデータソース設定変更、デプロイスキャン時の管理操作実行時エラー。",
         'annotation.errorCode = "WFLYCTL0013"\nまたは Logs Insights:\nfilter @message like /WFLYCTL0013/',
         "1. server.logの詳細 failure-description を確認。\n2. 設定XMLの構文不整合や未定義モジュール参照を解消。",
         "起動スクリプトやCI/CDパイプライン実行直後のログを集中的に確認。"),
        ("デプロイ・管理", "WFLYSRV0026\n(Server Subsystem)",
         "【症状】Failed to start service...\nJBoss起動時やWAR/EARデプロイ時に依存サービスやサブシステムの初期化に失敗。",
         'annotation.errorCode = "WFLYSRV0026"\nまたは Logs Insights:\nfilter @message like /WFLYSRV0026/',
         "1. 起動依存関係（Missing dependencies）の解決。\n2. JNDIバインディング名の typo やDB初期接続疎通を確認。",
         "起動時の一過性ログのため、デプロイ完了後は通常発生しない。"),

        # Webコンテナ・通信
        ("Web・通信", "UT005023\n(Undertow HTTP)",
         "【症状】Exception handling request to...\nJBossの内蔵WebサーバーUndertowがクライアントからのリクエストを処理中に未処理例外が発生。",
         'annotation.errorCode = "UT005023"\nまたは Logs Insights:\nfilter @message like /UT005023/',
         "1. 直後のスタックトレースから業務ロジックの例外を特定。\n2. 悪意あるリクエストや巨大リクエストボディの制限値確認。",
         "ヘルスチェック起因のエラーでないか、!http.url CONTAINS \"health\" で除外確認。"),
        ("Web・通信", "UT000020\n(Undertow Connection)",
         "【症状】Connection timed out / Connection reset\nクライアントとJBoss間のTCP接続が途中で切断されたか、アイドルタイムアウトに達した。",
         'annotation.errorCode = "UT000020"\nまたは Logs Insights:\nfilter @message like /UT000020/',
         "1. ALBのアイドルタイムアウト値（標準60秒）とJBossのUndertowタイムアウト値の整合性確認（ALBよりJBoss側を長く設定）。",
         "ユーザーのブラウザバックや画面閉じによる正常切断ノイズが多いため除外を検討。"),

        # トランザクション
        ("トランザクション", "ARJUNA016051\n(Narayana JTA)",
         "【症状】Thread is already associated with a transaction\n1つのワーカースレッドに複数のJTAトランザクションが多重アソシエーションされデッドロック状態。",
         'annotation.errorCode = "ARJUNA016051"\nまたは Logs Insights:\nfilter @message like /ARJUNA016051/',
         "1. EJBのトランザクション属性（REQUIRES_NEW, REQUIRED）の設定見直し。\n2. 別スレッドを不用意に生成してJTAコンテキストを共有していないか確認。",
         "トランザクションタイムアウト（ARJUNA016027）と連動して発生しやすい。"),

        # Java主要例外
        ("Java主要例外", "NullPointerException\n(java.lang)",
         "【症状】オブジェクト参照がnullの状態でメソッド呼び出しやフィールドアクセスを実行。\nJava開発で最もポピュラーかつ致命的なバグ。",
         'annotation.exception CONTAINS "NullPointerException"\nまたは Logs Insights:\nfilter @message like /NullPointerException/',
         "1. 直前のログから入力パラメータを確認。\n2. Optional の活用や null チェック防御コードの追加。\n3. 外部APIからのレスポンス構造変更がないか検証。",
         "単一のNPEが大量のHTTP 500を引き起こすため、Trace IDから最初のリクエストを特定。"),
        ("Java主要例外", "OutOfMemoryError\n(java.lang)",
         "【症状】Java heap space / Metaspace\nJVMヒープ領域またはメタスペースが満杯になり、新規オブジェクトの割り当てが不能。",
         'annotation.exception CONTAINS "OutOfMemoryError"\nまたは Logs Insights:\nfilter @message like /OutOfMemoryError/',
         "1. ECSタスク/EC2の緊急再起動。\n2. -XX:+HeapDumpOnOutOfMemoryError でヒープダンプ取得・Eclipse MATでメモリリーク分析。\n3. -Xmx の適正拡張。",
         "OOM発生直前のレスポンスタイム急増トレース（GC停止時間による遅延）を特定。"),
        ("Java主要例外", "SQLException /\nSQLTimeoutException",
         "【症状】データベース処理中のタイムアウト、デッドロック、構文エラー、接続切断。",
         'annotation.exception CONTAINS "SQLException"\nまたは Logs Insights:\nfilter @message like /SQLException/',
         "1. SQLステートメントとバインド変数の特定。\n2. DB側のスロークエリログ（RDS Performance Insights）と突き合わせ。\n3. 適切なDBインデックスの作成。",
         "ネットワーク瞬断による一時的切断（再試行可能）と構文エラーを切り分け。"),

        # ノイズ除外鉄板レシピ
        ("ノイズ除外レシピ", "ヘルスチェック・監視\n完全無害化フィルタ",
         "【背景】ALBやKubernetes、CloudWatch Syntheticsが数秒おきに叩くヘルスチェックがログの99%を占め、本物の障害が埋もれる。",
         "CloudWatch トレース:\nfault = true AND !http.url CONTAINS \"health\" AND NOT http.user_agent CONTAINS \"ELB\"\n\nLogs Insights:\nfilter @message not like /health/ and @message not like /ELB-HealthChecker/ and @message not like /kube-probe/",
         "すべての調査クエリの基本テンプレートとして末尾に付加することを強く推奨。",
         "万一ヘルスチェック自体が落ちているインシデントの場合はこの除外を外して実行。")
    ]

    for row_idx, rdata in enumerate(troubleshooting_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws5.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 4 else font_regular
            cell.fill = fill_code if col_idx == 4 else (row_fill if row_fill else PatternFill(fill_type=None))
            cell.alignment = align_code if col_idx == 4 else (align_center if col_idx in [1] else align_left)
            cell.border = code_border if col_idx == 4 else box_border
            
        ws5.row_dimensions[row_idx].height = 55 if "\n" in str(rdata[3]) else 32

    ws5.freeze_panes = "C5"
    ws5.auto_filter.ref = f"A4:F{len(troubleshooting_data) + 4}"

    print("Sheet 5 generated.")

    # ----------------------------------------------------
    # Sheet 6: 06_コンソール操作完全マニュアル
    # ----------------------------------------------------
    ws6 = wb.create_sheet(title="06_コンソール操作完全マニュアル")
    ws6.views.sheetView[0].showGridLines = True

    ws6.merge_cells("A1:E1")
    ws6["A1"] = "AWSマネジメントコンソール クエリ実行ステップバイステップ 操作マニュアル"
    ws6["A1"].font = font_title
    ws6["A1"].fill = fill_title
    ws6["A1"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws6.row_dimensions[1].height = 36

    ws6.merge_cells("A2:E2")
    ws6["A2"] = "画面のどこにクエリを貼り付け、どのボタンを押し、結果画面をどう読み解けばよいかを画面イメージ付きで徹底解説します。"
    ws6["A2"].font = font_subtitle
    ws6["A2"].fill = fill_title
    ws6["A2"].alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws6.row_dimensions[2].height = 20

    headers_ws6 = [
        ("Step", 8),
        ("操作フェーズ", 18),
        ("画面上の操作手順と場所", 40),
        ("入力内容・クエリ貼り付け例", 45),
        ("画面の反応・確認すべきポイント", 35)
    ]

    for col_idx, (h_name, width) in enumerate(headers_ws6, 1):
        cell = ws6.cell(row=4, column=col_idx, value=h_name)
        cell.font = font_tbl_hdr
        cell.fill = fill_tbl_hdr
        cell.alignment = align_center
        cell.border = hdr_border
        col_letter = get_column_letter(col_idx)
        ws6.column_dimensions[col_letter].width = width

    ws6.row_dimensions[4].height = 28

    manual_data = [
        (1, "コンソールログイン",
         "1. AWSマネジメントコンソールにログインします。\n2. 右上のリージョン選択で、システムが稼働しているリージョン（例: アジアパシフィック (東京) ap-northeast-1）を選択します。",
         "リージョン確認: ap-northeast-1 (東京)",
         "正しいリージョンを選択しないとトレースデータが空（0件）と表示されるため注意。"),
        (2, "トレース画面へ移動",
         "1. 画面上部の検索バーに「CloudWatch」と入力してサービスを開きます。\n2. 左側ナビゲーションメニューの「X-Ray トレース」または「アプリケーションの監視」>「トレース」をクリックします。",
         "URLパス:\n/cloudwatch/home?region=ap-northeast-1#xray:traces",
         "「トレースの検索」画面が開き、上部に検索バー（フィルター式入力欄）が表示されます。"),
        (3, "時間範囲の設定",
         "1. 画面右上にあるタイムピッカー（時間選択ドロップダウン）をクリックします。\n2. 障害発生時間に合わせて「過去15分」「過去1時間」「過去3時間」または「カスタム」で絶対時刻を指定します。",
         "推奨: 障害発生時刻を含む最小の時間枠（例: 過去1時間）",
         "時間範囲が広すぎるとスキャンに時間がかかります。まずは短めの時間で絞るのが鉄則。"),
        (4, "クエリの貼り付け",
         "1. チートシートから実行したいクエリをコピーします。\n2. 「トレースの検索」バーをクリックして貼り付け（Ctrl + V）します。",
         "貼り付け例:\nfault = true AND !http.url CONTAINS \"health\"",
         "シンタックスハイライトが適用され、構文エラーがある場合は検索バーが赤枠で警告されます。"),
        (5, "クエリの実行",
         "1. 検索バー右側の青色「実行」ボタン（または「トレースの検索」ボタン）をクリックします。\n2. キーボードの「Enter」キーを押すだけでも即座に実行されます。",
         "ショートカット: Enter キー",
         "検索が開始され、ローディングインジケーターが表示された後、数秒で結果が更新されます。"),
        (6, "結果画面の確認 (1)",
         "【散布図 (Scatter Plot) の確認】\n画面上部のグラフで、横軸（時刻）と縦軸（所要時間/秒）にドットがプロットされます。赤色（Fault）や黄色（Error）のドットが集中している時間帯を把握。",
         "赤色ドット: 5xx 障害\n黄色ドット: 4xx エラー\n緑色ドット: 正常",
         "特定の時間帯に赤色ドットが急増している場合、その時間帯をドラッグしてさらにズーム可能。"),
        (7, "結果画面の確認 (2)",
         "【トレースリストの確認】\nグラフの下に合致したトレース一覧が表示されます。「ID」「レスポンス時間」「ステータス」「URL」「クライアントIP」等の列を確認。",
         "遅延調査なら「レスポンス時間」列ヘッダーをクリックして降順ソート",
         "最も遅い、または最もエラーが重篤なトレースの「ID」リンクをクリックします。"),
        (8, "トレース詳細とタイムライン",
         "【タイムライン（ガントチャート）の分析】\nトレース詳細画面では、各サービスの呼び出し順序と処理時間が棒グラフで表示されます。どの区間（JBoss、DB、外部API）で棒が最も伸びているかを確認。",
         "バーが最も長い箇所 = ボトルネック\n赤色アイコンの箇所 = エラー発生源",
         "JBoss内部のDBアクセス（サブセグメント）が3秒かかっていれば、DBボトルネックと即断。"),
        (9, "ログとの連動 (ワンクリック)",
         "【関連ログ (Related logs) の閲覧】\n画面右側の「ログ (Logs)」タブをクリック、または各スパンをクリックして「関連するログを表示」を選択。",
         "自動的にCloudWatch Logs Insightsに遷移",
         "該当リクエストと完全に同一のTrace IDを持つJBossのログ（server.log）が自動抽出されます。"),
        (10, "Logs Insightsでの実行",
         "【ロググループ横断クエリの実行】\n1. CloudWatchメニューの「Logs Insights」を開きます。\n2. 上部のロググループ選択で「/aws/ecs/jboss-eap」等を選択。\n3. クエリ入力欄にシート03のクエリを貼り付けて「クエリの実行」をクリック。",
         "貼り付け例:\nfields @timestamp, @message\n| filter @message like /WFLYCTL/\n| limit 50",
         "ログメッセージが整形されて表形式で一覧表示され、詳細ログを深堀りできます。")
    ]

    for row_idx, rdata in enumerate(manual_data, 5):
        is_even = (row_idx % 2 == 0)
        row_fill = fill_zebra if is_even else None

        for col_idx, val in enumerate(rdata, 1):
            cell = ws6.cell(row=row_idx, column=col_idx, value=val)
            cell.font = font_code if col_idx == 4 and "filter" in str(val) else font_regular
            cell.fill = fill_code if col_idx == 4 and "filter" in str(val) else (row_fill if row_fill else PatternFill(fill_type=None))
            cell.alignment = align_left if col_idx >= 3 else align_center
            cell.border = box_border
            
        ws6.row_dimensions[row_idx].height = 48 if "\n" in str(rdata[2]) or "\n" in str(rdata[3]) else 28

    ws6.freeze_panes = "C5"
    ws6.auto_filter.ref = f"A4:E{len(manual_data) + 4}"

    print("Sheet 6 generated.")

    # Save Excel workbook
    wb.save(file_path)
    print(f"Workbook successfully saved to: {file_path}")

if __name__ == "__main__":
    out_xlsx = r"C:\Users\taka_\Agy\CWTrace_Agy\CloudWatch_Trace_Query_Cheatsheet.xlsx"
    build_excel_workbook(out_xlsx)
