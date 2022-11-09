echo on
cd ..
cd /qspectrumanalyzer

pyuic5 qspectrumanalyzer.ui -o ui_qspectrumanalyzer.py
pyuic5 qspectrumanalyzer_baseline.ui -o ui_qspectrumanalyzer_baseline.py
pyuic5 qspectrumanalyzer_colors.ui -o ui_qspectrumanalyzer_colors.py
pyuic5 qspectrumanalyzer_persistence.ui -o ui_qspectrumanalyzer_persistence.py
pyuic5 qspectrumanalyzer_settings_help.ui -o ui_qspectrumanalyzer_settings_help.py
pyuic5 qspectrumanalyzer_settings.ui -o ui_qspectrumanalyzer_settings.py
pyuic5 qspectrumanalyzer_smoothing.ui -o ui_qspectrumanalyzer_smoothing.py

pause
