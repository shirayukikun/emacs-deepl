(setq emacs-deepl-file-path (file-name-directory load-file-name))
(setq emacs-deepl-config-list (json-read-file (concat emacs-deepl-file-path "config.json")))
(setq emacs-deepl-python-code-path (concat emacs-deepl-file-path "DeepL_api_connect.py"))
(setq emacs-pdf-translation-python-code-path (concat emacs-deepl-file-path "DeepL_pdf_translation.py"))

(setq deepl-authorization-key (cdr (nth 0 emacs-deepl-config-list)))
(setq pdf-to-text-api-key (cdr (nth 1 emacs-deepl-config-list)))


;; *DeepL*という, 翻訳結果を出力するバッファを生成する
(defun create-DeppL_output-buffer(translate-result)
  (set-buffer (get-buffer-create "*DeepL*"))
  (goto-char (point-max))
  (insert translate-result)
  (display-buffer (get-buffer-create "*DeepL*"))
  )


;; 選択された範囲の翻訳を行う
(defun DeepL-translate-region (begin end)
  (interactive "r")
  (when (use-region-p)
    (save-excursion
      (create-DeppL_output-buffer
       (shell-command-to-string 
	(concat
	 "python " 
	 emacs-deepl-python-code-path
	 " -t \""
	 (buffer-substring-no-properties begin end)
	 "\" -d \""
	 deepl-authorization-key
	 "\""
	 )))
      )
    )
  )


;; ミニバッファに単語や文を入力し翻訳を行う
(defun DeepL-translate(source_text)
  (interactive "s")
  (save-excursion
    (create-DeppL_output-buffer
     (shell-command-to-string 
      (concat
       "python " 
       emacs-deepl-python-code-path
       " -t \""
       source_text 
       "\" -d \""
       deepl-authorization-key
       "\""
       )))
    ) 
  )



;; カレントバッファで開いているpdfファイルを翻訳する
(defun DeepL-translate-pdf()
  (interactive)
  (save-excursion
    (create-DeppL_output-buffer
     (shell-command-to-string 
      (concat
       "python " 
       emacs-pdf-translation-python-code-path
       " -f \""
       buffer-file-name
       "\" -d \""
       deepl-authorization-key
       "\" -p \""
       pdf-to-text-api-key
       "\""
       )))
    ) 
  )


