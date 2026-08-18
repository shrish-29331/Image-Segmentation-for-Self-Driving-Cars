# Assignment Auto Grader Portal

A **Streamlit-based web portal** for seamless assignment submission and automatic evaluation. It provides dedicated interfaces for both students and evaluators (TAs), making the grading process efficient, secure, and insightful.

---

##  Features

### 1.  Authentication & File Upload  
- Students securely log in and upload multiple files per assignment.  
- Ensures confidentiality and streamlines the submission process.

### 2.  Late Submission Detection  
- Automatically checks submission time against assignment deadlines.  
- Flags late submissions for evaluators.

### 3.  Plagiarism Detection  
Evaluators can check for code similarity using a **custom-built plagiarism checker**.  
A match is flagged if similarity exceeds a defined threshold.

**How it works:**
-  **Porter Stemming** to normalize text  
-  **TF-IDF Vectorization**  
-  **Cosine Similarity** for comparison

### 4. Auto-Grading with Test Cases  
- Runs submitted code against provided test cases.  
- Compares outputs and shows pass/fail status.  
- Displays any syntax errors for quick debugging.

### 5.  Review & Feedback  
The system evaluates:
- 75 points for Test Case Accuracy  
- 25 points for Code Quality & Documentation

**C++ Code Quality Metrics:**
-  Comment-to-code ratio  
-  Expression complexity  
-  Indentation issues  
-  Repetition  
-  Variable naming & scoping

> Python files are analyzed using `pylint`; C++ analysis is custom-built.

### 6.  No External APIs  
- No third-party APIs used  
- All logic is written from scratch for **plagiarism** and **code analysis**

---

##  Future Updates

1. **Multi-language Support:** Add Java, JavaScript, etc.  
2. **Mobile App:** Android/iOS app for submission and grading.

---

##  Sample Credentials

###  Student Accounts:
| Username     | Password   |
|--------------|------------|
| `s001`  | `password` |
| `s002`       | `password` |

### TA Accounts:
| Username     | Password   |
|--------------|------------|
| `ta001`      | `password` |
| `ta002`      | `password` |

---

##  Installation

###  Requirements
- Python 3.10

###  Install Dependencies
```bash
pip install -r requirements.txt
```
Run using
```
streamlit run Login.py
```
### Contributors

Jaismeen Kaur – 230121030

Shrish Uttarwar – 230101108



