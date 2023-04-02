# (C) Copyright 2005-2023 Enthought, Inc., Austin, TX
# All rights reserved.
#
# This software is provided without warranty under the terms of the BSD
# license included in LICENSE.txt and may be redistributed only under
# the conditions described in the aforementioned license. The license
# is also available online at http://www.enthought.com/licenses/BSD.txt
#
# Thanks for using Enthought open source!

from contextlib import closing
from os import stat
try:
    from importlib.resources import files
except ImportError:
    from importlib_resources import files
from pathlib import Path
import shutil
import tempfile
import time
import unittest
from zipfile import ZipFile, ZIP_DEFLATED

from pyface.image_resource import ImageResource
from pyface.ui_traits import Border, Margin
from ..image import (
    FastZipFile, ImageLibrary, ImageVolume, ImageVolumeInfo, ZipFileReference,
    join_image_name, split_image_name, time_stamp_for,
)


LIBRARY_DIR = files('pyface.image') / "library"
ICONS_FILE = LIBRARY_DIR / "icons.zip"
TEST_IMAGES_DIR = files('pyface.tests') / "images"


class TestJoinImageName(unittest.TestCase):

    def test_simple(self):
        image_name = join_image_name("icons", "red_ball.jpg")

        self.assertEqual(image_name, "@icons:red_ball.jpg")

    def test_extension(self):
        image_name = join_image_name("icons", "red_ball.png")

        self.assertEqual(image_name, "@icons:red_ball")

    def test_double_extension(self):
        image_name = join_image_name("icons", "red_ball.foo.png")

        self.assertEqual(image_name, "@icons:red_ball.foo.png")


class TestSplitImageName(unittest.TestCase):

    def test_simple(self):
        volume_name, file_name = split_image_name("@icons:red_ball.jpg")

        self.assertEqual(volume_name, "icons")
        self.assertEqual(file_name, "red_ball.jpg")

    def test_extension(self):
        volume_name, file_name = split_image_name("@icons:red_ball")

        self.assertEqual(volume_name, "icons")
        self.assertEqual(file_name, "red_ball.png")

    def test_no_at_symbol(self):
        volume_name, file_name = split_image_name("icons:red_ball.jpg")

        # XXX this should probably raise rather than doing this
        self.assertEqual(volume_name, "cons")
        self.assertEqual(file_name, "red_ball.jpg")

    def test_no_colon(self):
        volume_name, file_name = split_image_name("@red_ball.jpg")

        # XXX this should probably raise rather than doing this
        self.assertEqual(volume_name, "red_ball.jp")
        self.assertEqual(file_name, "@red_ball.jpg")

    def test_no_colon_or_at_symbol(self):
        volume_name, file_name = split_image_name("red_ball.jpg")

        # XXX this should probably raise rather than doing this
        self.assertEqual(volume_name, "ed_ball.jp")
        self.assertEqual(file_name, "red_ball.jpg")


class TestFastZipFile(unittest.TestCase):

    def test_read_icons_red_ball(self):
        zf = FastZipFile(path=ICONS_FILE)

        file_bytes = zf.read("red_ball.png")

        self.assertTrue(file_bytes.startswith(b"\x89PNG"))

    def test_namelist_icons(self):
        zf = FastZipFile(path=ICONS_FILE)

        names = zf.namelist()

        self.assertTrue("red_ball.png" in names)
        self.assertEqual(names, zf.zf.namelist())

    def test_close_icons(self):
        zf = FastZipFile(path=ICONS_FILE)

        actual_zf = zf.zf

        self.assertIs(zf._zf, actual_zf)

        zf.close()

        self.assertIsNone(zf._zf)

    def test_eventual_zipfile_close(self):
        zf = FastZipFile(path=ICONS_FILE)

        self.assertFalse(zf._running)
        start_time = time.time()

        actual_zf = zf.zf

        end_time = time.time()

        self.assertIsNotNone(actual_zf)
        self.assertGreaterEqual(zf.time_stamp, start_time)
        self.assertLessEqual(zf.time_stamp, end_time)
        self.assertTrue(zf._running)
        self.assertIs(zf._zf, actual_zf)

        # wait for thread to clean-up zipfile
        # XXX this is not nice
        while time.time() <= end_time + 3.0:
            time.sleep(1.0)

        self.assertFalse(zf._running)
        self.assertIsNone(zf._zf)


class TestImageVolume(unittest.TestCase):

    def test_init_empty(self):
        volume = ImageVolume()

        self.assertEqual(volume.name, "")
        self.assertEqual(volume.images, [])
        self.assertEqual(volume.catalog, {})
        self.assertEqual(volume.category, "General")
        self.assertEqual(volume.keywords, [])
        self.assertEqual(volume.aliases, [])
        self.assertEqual(volume.path, "")
        self.assertTrue(volume.is_zip_file)
        self.assertIsNone(volume.zip_file)
        self.assertEqual(volume.time_stamp, "")
        self.assertEqual(len(volume.info), 1)
        self.assertIsInstance(volume.info[0], ImageVolumeInfo)

    def test_empty_zipfile(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test.zip"
            ZipFile(path, "w", ZIP_DEFLATED).close()
            with closing(FastZipFile(path=path)) as zf:
                time_stamp = time_stamp_for(stat(path).st_mtime)

                volume = ImageVolume(name="test", path=path, zip_file=zf)

                self.assertEqual(volume.name, "test")
                self.assertEqual(volume.images, [])
                self.assertEqual(volume.catalog, {})
                self.assertEqual(volume.category, "General")
                self.assertEqual(volume.keywords, [])
                self.assertEqual(volume.aliases, [])
                self.assertEqual(Path(volume.path), path)
                self.assertTrue(volume.is_zip_file)
                self.assertIs(volume.zip_file, zf)
                self.assertEqual(volume.time_stamp, time_stamp)
                self.assertEqual(len(volume.info), 1)
                self.assertIsInstance(volume.info[0], ImageVolumeInfo)

    def test_empty_directory(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test"
            path.mkdir()
            time_stamp = time_stamp_for(stat(path).st_mtime)

            volume = ImageVolume(name="test", path=path, is_zip_file=False)

            self.assertEqual(volume.name, "test")
            self.assertEqual(volume.images, [])
            self.assertEqual(volume.catalog, {})
            self.assertEqual(volume.category, "General")
            self.assertEqual(volume.keywords, [])
            self.assertEqual(volume.aliases, [])
            self.assertEqual(Path(volume.path), path)
            self.assertFalse(volume.is_zip_file)
            self.assertIsNone(volume.zip_file)
            self.assertEqual(volume.time_stamp, time_stamp)
            self.assertEqual(len(volume.info), 1)
            self.assertIsInstance(volume.info[0], ImageVolumeInfo)

    def test_empty_directory_save(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test"
            path.mkdir()
            time_stamp = time_stamp_for(stat(path).st_mtime)

            volume = ImageVolume(name="test", path=path, is_zip_file=False)
            result = volume.save()

            self.assertTrue(result)

            filenames = {file.name for file in path.iterdir()}
            self.assertEqual(filenames, {"image_volume.py", "image_info.py", "license.txt"})

            # test that new file is readable
            time_stamp = time_stamp_for(stat(path).st_mtime)

            volume_2 = ImageVolume(name="test", path=path, is_zip_file=False)

            self.assertEqual(volume_2.name, "test")
            self.assertEqual(volume_2.images, [])
            self.assertEqual(volume_2.catalog, {})
            self.assertEqual(volume_2.category, "General")
            self.assertEqual(volume_2.keywords, [])
            self.assertEqual(volume_2.aliases, [])
            self.assertEqual(Path(volume_2.path), path)
            self.assertFalse(volume_2.is_zip_file)
            self.assertIsNone(volume_2.zip_file)
            self.assertEqual(volume_2.time_stamp, time_stamp)
            self.assertEqual(len(volume_2.info), 1)
            self.assertIsInstance(volume_2.info[0], ImageVolumeInfo)

    def test_empty_zipfile_save(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test.zip"
            ZipFile(path, "w", ZIP_DEFLATED).close()
            with closing(FastZipFile(path=path)) as zf:
                time_stamp = time_stamp_for(stat(path).st_mtime)

                volume = ImageVolume(name="test", path=path, zip_file=zf)

                result = volume.save()

            self.assertTrue(result)

            with closing(FastZipFile(path=path)) as zf:
                self.assertEqual(set(zf.namelist()), {"image_volume.py", "image_info.py", "license.txt"})

            # test that new file is readable
            with closing(FastZipFile(path=path)) as zf:
                time_stamp = time_stamp_for(stat(path).st_mtime)

                volume_2 = ImageVolume(name="test", path=path, zip_file=zf)

                self.assertEqual(volume_2.name, "test")
                self.assertEqual(volume_2.images, [])
                self.assertEqual(volume_2.catalog, {})
                self.assertEqual(volume_2.category, "General")
                self.assertEqual(volume_2.keywords, [])
                self.assertEqual(volume_2.aliases, [])
                self.assertEqual(Path(volume_2.path), path)
                self.assertTrue(volume_2.is_zip_file)
                self.assertIs(volume_2.zip_file, zf)
                self.assertEqual(volume_2.time_stamp, time_stamp)
                self.assertEqual(len(volume_2.info), 1)
                self.assertIsInstance(volume_2.info[0], ImageVolumeInfo)

    def test_save_directory(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test"
            path.mkdir()
            time_stamp = time_stamp_for(stat(path).st_mtime)
            image_file = path / "core.png"
            shutil.copyfile(TEST_IMAGES_DIR / "core.png", image_file)

            # this should create an default ImageInfo object for the image
            # file as a side-effect of loading.
            volume = ImageVolume(name="test", path=path, is_zip_file=False)

            self.assertEqual(len(volume.images), 1)
            self.assertGreaterEqual(volume.time_stamp, time_stamp)

            image = volume.images[0]
            self.assertEqual(image.image_name, "@test:core")
            self.assertEqual(image.name, "core")
            self.assertEqual(image.volume, volume)
            self.assertEqual(image.description, "")
            self.assertEqual(image.category, "General")
            self.assertEqual(image.keywords, [])
            self.assertEqual(image.width, 64)
            self.assertEqual(image.height, 64)
            self.assertIsInstance(image.border, Border)
            self.assertIsInstance(image.content, Margin)
            self.assertIsInstance(image.label, Margin)
            self.assertEqual(image.alignment, "default")
            self.assertEqual(image.copyright, 'No copyright information specified.')

            result = volume.save()

            self.assertTrue(result)

            filenames = {file.name for file in path.iterdir()}
            self.assertEqual(filenames, {"core.png", "image_volume.py", "image_info.py", "license.txt"})

            # test that new file is readable
            time_stamp = time_stamp_for(stat(path).st_mtime)

            volume_2 = ImageVolume(name="test", path=path, is_zip_file=False)

            self.assertEqual(volume_2.name, "test")
            self.assertEqual(len(volume_2.images), 1)
            self.assertEqual(len(volume_2.catalog), 1)
            self.assertIn("@test:core", volume_2.catalog)
            self.assertEqual(volume_2.category, "General")
            self.assertEqual(volume_2.keywords, [])
            self.assertEqual(volume_2.aliases, [])
            self.assertEqual(Path(volume_2.path), path)
            self.assertFalse(volume_2.is_zip_file)
            self.assertIsNone(volume_2.zip_file)
            self.assertEqual(volume_2.time_stamp, time_stamp)
            self.assertEqual(len(volume_2.info), 1)
            self.assertIsInstance(volume_2.info[0], ImageVolumeInfo)

            image = volume_2.images[0]
            self.assertEqual(image.image_name, "@test:core")
            self.assertEqual(image.name, "core")
            self.assertEqual(image.volume, volume_2)
            self.assertEqual(image.description, "")
            self.assertEqual(image.category, "General")
            self.assertEqual(image.keywords, [])
            self.assertEqual(image.width, 64)
            self.assertEqual(image.height, 64)
            self.assertIsInstance(image.border, Border)
            self.assertIsInstance(image.content, Margin)
            self.assertIsInstance(image.label, Margin)
            self.assertEqual(image.alignment, "default")
            self.assertEqual(image.copyright, 'No copyright information specified.')

            # do one more save to smoke-test other code paths
            volume_2.save()

    def test_save_zipfile(self):
        with tempfile.TemporaryDirectory() as dir_path:
            path = Path(dir_path) / "test.zip"
            with ZipFile(path, "w", ZIP_DEFLATED) as zf:
                zf.write(TEST_IMAGES_DIR / "core.png", "core.png")

            with closing(FastZipFile(path=path)) as zf:
                time_stamp = time_stamp_for(stat(path).st_mtime)

                # this should create an default ImageInfo object for the image
                # file as a side-effect of loading.
                volume = ImageVolume(name="test", path=path, zip_file=zf)

                self.assertEqual(len(volume.images), 1)
                self.assertGreaterEqual(volume.time_stamp, time_stamp)

                image = volume.images[0]
                self.assertEqual(image.image_name, "@test:core")
                self.assertEqual(image.name, "core")
                self.assertEqual(image.volume, volume)
                self.assertEqual(image.description, "")
                self.assertEqual(image.category, "General")
                self.assertEqual(image.keywords, [])
                self.assertEqual(image.width, 64)
                self.assertEqual(image.height, 64)
                self.assertIsInstance(image.border, Border)
                self.assertIsInstance(image.content, Margin)
                self.assertIsInstance(image.label, Margin)
                self.assertEqual(image.alignment, "default")
                self.assertEqual(image.copyright, 'No copyright information specified.')

                result = volume.save()

            self.assertTrue(result)

            with closing(FastZipFile(path=path)) as zf:
                self.assertEqual(set(zf.namelist()), {"core.png", "image_volume.py", "image_info.py", "license.txt"})

            # test that new file is readable
            with closing(FastZipFile(path=path)) as zf:
                time_stamp = time_stamp_for(stat(path).st_mtime)

                volume_2 = ImageVolume(name="test", path=path, zip_file=zf)

                self.assertEqual(volume_2.name, "test")
                self.assertEqual(len(volume_2.images), 1)
                self.assertEqual(len(volume_2.catalog), 1)
                self.assertIn("@test:core", volume_2.catalog)
                self.assertEqual(volume_2.category, "General")
                self.assertEqual(volume_2.keywords, [])
                self.assertEqual(volume_2.aliases, [])
                self.assertEqual(Path(volume_2.path), path)
                self.assertTrue(volume_2.is_zip_file)
                self.assertIs(volume_2.zip_file, zf)
                self.assertEqual(volume_2.time_stamp, time_stamp)
                self.assertEqual(len(volume_2.info), 1)
                self.assertIsInstance(volume_2.info[0], ImageVolumeInfo)

                image = volume_2.images[0]
                self.assertEqual(image.image_name, "@test:core")
                self.assertEqual(image.name, "core")
                self.assertEqual(image.volume, volume_2)
                self.assertEqual(image.description, "")
                self.assertEqual(image.category, "General")
                self.assertEqual(image.keywords, [])
                self.assertEqual(image.height, 64)
                self.assertEqual(image.width, 64)
                self.assertIsInstance(image.border, Border)
                self.assertIsInstance(image.content, Margin)
                self.assertIsInstance(image.label, Margin)
                self.assertEqual(image.alignment, "default")
                self.assertEqual(image.copyright, 'No copyright information specified.')

                # do one more save to smoke-test other code paths
                volume_2.save()

    def test_icons_zipfile_volume(self):
        time_stamp = time_stamp_for(stat(ICONS_FILE).st_mtime)
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            self.assertEqual(volume.name, "icons")
            self.assertTrue(
                any(
                    image.image_name == "@icons:red_ball"
                    for image in volume.images
                )
            )
            self.assertTrue("@icons:red_ball" in volume.catalog)
            self.assertEqual(volume.category, "General")
            self.assertEqual(volume.keywords, [])
            self.assertEqual(volume.aliases, [])
            self.assertEqual(Path(volume.path), ICONS_FILE)
            self.assertTrue(volume.is_zip_file)
            self.assertIs(volume.zip_file, zf)
            self.assertEqual(volume.time_stamp, time_stamp)
            self.assertEqual(len(volume.info), 1)
            self.assertIsInstance(volume.info[0], ImageVolumeInfo)

    def test_icons_image_resource(self):
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            image = volume.image_resource("@icons:red_ball")

        self.assertIsInstance(image, ImageResource)
        self.assertIsInstance(image._ref, ZipFileReference)
        self.assertTrue(ICONS_FILE.samefile(image._ref.path))

    def test_icons_image_resource_missing(self):
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            image = volume.image_resource("@icons:does_not_exist")

        self.assertIsInstance(image, ImageResource)
        self.assertIsInstance(image._ref, ZipFileReference)
        self.assertTrue(ICONS_FILE.samefile(image._ref.path))

    def test_icons_image_data(self):
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            data = volume.image_data("@icons:red_ball")

        self.assertTrue(data.startswith(b"\x89PNG"))

    def test_icons_image_data_missing(self):
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            with self.assertRaises(KeyError):
                volume.image_data("@icons:does_not_exist")

    def test_icons_volume_info(self):
        with closing(FastZipFile(path=ICONS_FILE)) as zf:
            volume = ImageVolume(name="icons", path=ICONS_FILE, zip_file=zf)

            volume_info = volume.volume_info("@icons:red_ball")

        self.assertIs(volume_info, volume.info[0])

    def test_volume_info(self):
        volume = ImageVolume(
            name="test",
            info=[
                ImageVolumeInfo(image_names=["@test:one", "@test:two"]),
                ImageVolumeInfo(image_names=["@test:three", "@test:two"]),
            ]
        )

        volume_info = volume.volume_info("@test:two")
        self.assertIs(volume_info, volume.info[0])

        volume_info = volume.volume_info("@test:three")
        self.assertIs(volume_info, volume.info[1])

        with self.assertRaises(ValueError):
            volume.volume_info("@test:four")


class TestImageLibrary(unittest.TestCase):

    # XXX These are more in the flavor of integration tests

    def test_default_volumes(self):
        volume_names = {volume.name for volume in ImageLibrary.volumes}
        self.assertEqual(volume_names, {'icons', 'std'})

    def test_default_catalog(self):
        self.assertEqual(set(ImageLibrary.catalog.keys()), {'icons', 'std'})

    def test_default_images(self):
        image_names = {image.image_name for image in ImageLibrary.images}
        self.assertTrue("@icons:red_ball" in image_names)

    def test_image_info(self):
        red_ball_image_info = ImageLibrary.image_info("@icons:red_ball")

        self.assertEqual(red_ball_image_info.name, "red_ball")
        self.assertEqual(red_ball_image_info.image_name, "@icons:red_ball")
        self.assertEqual(red_ball_image_info.width, 16)
        self.assertEqual(red_ball_image_info.height, 16)

    def test_image_info_missing(self):
        missing_image_info = ImageLibrary.image_info("@icons:does_not_exist")

        self.assertIsNone(missing_image_info)

    def test_image_info_volume_missing(self):
        missing_image_info = ImageLibrary.image_info("@missing:does_not_exist")

        self.assertIsNone(missing_image_info)

    def test_image_resource(self):
        red_ball_image = ImageLibrary.image_resource("@icons:red_ball")

        self.assertIsInstance(red_ball_image, ImageResource)
        self.assertIsInstance(red_ball_image._ref, ZipFileReference)
        self.assertTrue(ICONS_FILE.samefile(red_ball_image._ref.path))

    def test_image_resource_missing(self):
        missing_image = ImageLibrary.image_info("@icons:does_not_exist")

        self.assertIsNone(missing_image)

    def test_image_resource_missing_volume(self):
        missing_image = ImageLibrary.image_info("@missing:does_not_exist")

        self.assertIsNone(missing_image)

    def test_find_volume(self):
        volume = ImageLibrary.find_volume("@icons:red_ball")

        self.assertIsInstance(volume, ImageVolume)
        self.assertEqual(volume.name, "icons")
        self.assertTrue(ICONS_FILE.samefile(volume.path))
