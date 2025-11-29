import 'package:flutter/cupertino.dart';
import '../../core/api_client.dart';

class UploadPage extends StatefulWidget {
  const UploadPage({super.key});

  @override
  State<UploadPage> createState() => _UploadPageState();
}

class _UploadPageState extends State<UploadPage> {
  final _titleController = TextEditingController();
  final _descController = TextEditingController();
  bool _loading = false;
  String? _result;

  @override
  void dispose() {
    _titleController.dispose();
    _descController.dispose();
    super.dispose();
  }

  Future<void> _submit() async {
    setState(() {
      _loading = true;
      _result = null;
    });

    try {
      final api = ApiClient();
      final res = await api.postJson('/news/upload', data: {
        'title': _titleController.text.trim(),
        'description': _descController.text.trim(),
      });
      setState(() {
        _result = res.data.toString();
      });
    } catch (e) {
      setState(() {
        _result = 'Error: $e';
      });
    } finally {
      setState(() {
        _loading = false;
      });
    }
  }

  @override
  Widget build(BuildContext context) {
    return CupertinoPageScaffold(
      navigationBar: const CupertinoNavigationBar(
        middle: Text('Upload News'),
      ),
      child: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(20),
          child: Column(
            children: [
              CupertinoTextField(
                controller: _titleController,
                placeholder: 'Title',
              ),
              const SizedBox(height: 16),
              CupertinoTextField(
                controller: _descController,
                placeholder: 'Description',
                maxLines: 4,
              ),
              const SizedBox(height: 24),
              CupertinoButton.filled(
                onPressed: _loading ? null : _submit,
                child: _loading
                    ? const CupertinoActivityIndicator()
                    : const Text('Verify & Upload'),
              ),
              const SizedBox(height: 16),
              if (_result != null)
                Expanded(
                  child: SingleChildScrollView(
                    child: Text(
                      _result!,
                      style: const TextStyle(fontSize: 12),
                    ),
                  ),
                ),
            ],
          ),
        ),
      ),
    );
  }
}
