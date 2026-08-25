Logger Configuration
====================

SpectraLog is configured through :func:`spectralog.CreateSpectraLogger`.

Core Configuration
------------------

.. code-block:: python

   logger = CreateSpectraLogger(
       debug_mode=False,
       show_datetime=True,
       show_line=False,
       show_folder_name=False,
       logs_directory="logs",
       log_file_name=None,
       save_logs=True,
       multiprocessing_safe=False,
   )

Logging Level
-------------

``debug_mode=False`` uses INFO as the effective logging threshold.

``debug_mode=True`` uses DEBUG.

File Location
-------------

The default logging directory is:

.. code-block:: text

   logs/

A custom directory may be supplied:

.. code-block:: python

   logger = CreateSpectraLogger(
       logs_directory="/var/log/my-application",
   )

Custom File Name
----------------

.. code-block:: python

   logger = CreateSpectraLogger(
       log_file_name="application.log",
   )

When no file name is supplied, SpectraLog generates a daily log file.

Source Information
------------------

Include source paths:

.. code-block:: python

   logger = CreateSpectraLogger(
       show_folder_name=True,
   )

Include source line numbers:

.. code-block:: python

   logger = CreateSpectraLogger(
       show_line=True,
   )

Both options may be enabled together:

.. code-block:: python

   logger = CreateSpectraLogger(
       show_folder_name=True,
       show_line=True,
   )

Custom Formats
--------------

Use ``console_format`` or ``file_format`` when the generated format does not
meet application requirements.

.. code-block:: python

   logger = CreateSpectraLogger(
       console_format="%(levelname)s | %(message)s",
       file_format="%(asctime)s | %(levelname)s | %(message)s",
   )

Log Rotation
------------

SpectraLog uses rotating file handlers.

.. code-block:: python

   logger = CreateSpectraLogger(
       max_bytes=10 * 1024 * 1024,
       backup_count=5,
   )

``max_bytes`` controls the maximum active file size before rollover.

``backup_count`` controls the number of rotated files retained.
